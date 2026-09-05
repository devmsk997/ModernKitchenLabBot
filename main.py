from __future__ import annotations

import argparse
import html
import json
import re
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from pathlib import Path

from blogger.blogger_upload import list_existing_posts, save_publish_receipt, upload_to_blogger
from config import DAILY_POST_TIME, HISTORY_FILE, POST_AS_DRAFT, PREVIEW_DIR, SITE_NAME, TIMEZONE_NAME
from content.content_pipeline import run_content_pipeline
from content.quality_guard import simhash64
from seo_keyword.keyword_pipeline import run_keyword_pipeline
from seo_keyword.topic_clusters import select_cluster


def resolve_publish_target(clock_text: str | None = None) -> datetime:
    """Return the next local publish target in the configured site timezone."""
    clock_text = (clock_text or DAILY_POST_TIME or "21:00").strip()
    try:
        hour, minute = [int(x) for x in clock_text.split(":", 1)]
    except Exception as exc:
        raise ValueError(f"Invalid publish time: {clock_text}. Use HH:MM, e.g. 21:00") from exc
    tz = ZoneInfo(TIMEZONE_NAME)
    now = datetime.now(tz)
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    # If preparation somehow starts after today's deadline, never back-date a post.
    if target <= now:
        target += timedelta(days=1)
    return target


def _parse_rfc3339(value: str) -> datetime | None:
    value = (value or "").strip()
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def find_existing_scheduled_target(existing_posts: list[dict], target: datetime) -> dict | None:
    """Return a Blogger scheduled post already occupying this target slot."""
    for post in existing_posts:
        if (post.get("status") or "").lower() != "scheduled":
            continue
        dt = _parse_rfc3339(post.get("published", ""))
        if dt is None:
            continue
        try:
            local = dt.astimezone(target.tzinfo)
        except Exception:
            continue
        if abs((local - target).total_seconds()) <= 180:
            return post
    return None


def load_history() -> list[dict]:
    try:
        data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_history(history: list[dict]) -> None:
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.write_text(json.dumps(history[-1000:], indent=2, ensure_ascii=False), encoding="utf-8")


def get_existing_posts(allow_offline: bool) -> list[dict]:
    try:
        return list_existing_posts()
    except Exception as exc:
        if not allow_offline:
            raise
        print(f"Blogger history unavailable; using local history only: {exc}")
        return []


def write_preview(post: dict, keyword_data: dict) -> Path:
    """Write a clean reader-facing preview that mirrors the Blogger post body.

    SEO diagnostics stay in the console; they are intentionally not rendered inside
    the preview or published article.
    """
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = PREVIEW_DIR / f"preview-{stamp}.html"
    meta = post.get("meta_description", "")
    safe_title = html.escape(post["title"])
    safe_meta = html.escape(meta, quote=True)
    body = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{safe_title}</title>
<meta name="description" content="{safe_meta}">
<style>
body{{font-family:Arial,sans-serif;max-width:900px;margin:32px auto;padding:0 18px;line-height:1.7;color:#222}}
h1{{font-family:Georgia,serif;line-height:1.2}}
h2{{margin-top:34px}}
h3{{margin-top:24px}}
img{{max-width:100%;height:auto}}
a{{text-decoration:none}}
</style>
</head>
<body>
<h1>{safe_title}</h1>
{post['content']}
</body>
</html>"""
    path.write_text(body, encoding="utf-8")
    return path


def run(publish: bool = False, force_draft: bool | None = None, schedule_for: datetime | None = None) -> dict:
    print("\n========================================")
    print(f" {SITE_NAME.upper()} ORGANIC TOPIC-CLUSTER BOT")
    print("========================================")

    existing_posts = get_existing_posts(allow_offline=not publish)
    history = load_history()

    if publish and schedule_for is not None:
        occupied = find_existing_scheduled_target(existing_posts, schedule_for)
        if occupied:
            print("\n✅ TARGET SLOT ALREADY SCHEDULED IN BLOGGER")
            print("Scheduled for:", schedule_for.isoformat())
            print("Existing title:", occupied.get("title", ""))
            print("No duplicate article/image was generated.")
            return {
                "published": True,
                "scheduled": True,
                "already_scheduled": True,
                "scheduled_for": schedule_for.isoformat(),
                "blogger_response": occupied,
            }
    existing_titles = [p.get("title", "") for p in existing_posts]
    existing_titles.extend(h.get("title", "") for h in history)
    existing_keywords = [h.get("keyword", "") for h in history if h.get("keyword")]

    cluster = select_cluster(existing_posts, history)
    print("Selected cluster:", cluster["name"])
    print("Cluster coverage:", cluster["coverage"], "existing items")
    print("Content role:", cluster["content_role"])

    keyword_data = run_keyword_pipeline(existing_titles, existing_keywords, cluster=cluster)
    keyword = keyword_data["keyword"]
    topic = cluster["name"]

    used_image_sources = [h.get("image_source_url", "") for h in history if h.get("image_source_url")]
    # Recover prior Wikimedia source-credit links from existing Blogger HTML when available.
    for existing in existing_posts:
        body = existing.get("content", "") or ""
        used_image_sources.extend(
            re.findall(r'href=["\'](https?://commons\.wikimedia\.org/[^"\']+)["\']', body, flags=re.I)
        )
    used_image_sources = list(dict.fromkeys(x for x in used_image_sources if x))
    used_image_hashes = [h.get("image_source_sha256", "") for h in history if h.get("image_source_sha256")]
    used_image_pageids = [h.get("image_pageid") for h in history if h.get("image_pageid") is not None]
    used_image_public_urls = [u for p in existing_posts for u in (p.get("images") or []) if u]
    used_image_public_urls.extend(h.get("feature_image_url", "") for h in history if h.get("feature_image_url"))
    existing_content_hashes = [simhash64(p.get("content", "")) for p in existing_posts if p.get("content")]

    post = run_content_pipeline(
        topic,
        keyword,
        cluster,
        existing_posts=existing_posts,
        history=history,
        used_image_sources=used_image_sources,
        used_image_hashes=used_image_hashes,
        used_image_pageids=used_image_pageids,
        used_image_public_urls=used_image_public_urls,
        existing_content_hashes=existing_content_hashes,
    )
    preview_path = write_preview(post, keyword_data)

    print("\n===== SEO PACKAGE =====")
    print("Title/H1:", post["title"])
    print("Meta/Search-description candidate:", post["meta_description"])
    print("Custom permalink target:", post["permalink"])
    print("Labels:", ", ".join(post["labels"]))
    print("Content simhash:", post.get("content_simhash"))
    print("Feature image URL:", post.get("feature_image_url") or "not publicly hosted")
    if post.get("feature_image"):
        print("Feature image provider:", post["feature_image"].get("provider"))
        print("Feature image model:", post["feature_image"].get("model"))
        print("Feature image SHA-256:", post["feature_image"].get("source_sha256"))
    print("Preview:", preview_path)

    result = {
        "keyword": keyword,
        "keyword_data": keyword_data,
        "topic": topic,
        "cluster": cluster,
        "post": post,
        "preview": str(preview_path),
        "published": False,
    }

    if publish:
        is_draft = POST_AS_DRAFT if force_draft is None else force_draft
        schedule_iso = None
        if schedule_for is not None and not is_draft:
            schedule_iso = schedule_for.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        response = upload_to_blogger(post, is_draft=is_draft, schedule_at=schedule_iso)
        receipt = PREVIEW_DIR / "last_publish.json"
        save_publish_receipt(response, receipt)
        if schedule_iso:
            print("\n✅ BLOGGER POST SCHEDULED")
            print("Publish time:", schedule_for.isoformat())
            print("Blogger status:", response.get("status", "scheduled"))
        else:
            print("\n✅ BLOGGER POST CREATED")
            print("Mode:", "DRAFT" if is_draft else "LIVE")
        print("URL:", response.get("url"))
        print("Permalink status:", response.get("permalink_status"))
        print("Labels set through API:", ", ".join(response.get("labels", [])))
        print("Search Description: generated; Blogger API does not reliably expose the editor's per-post field.")
        result["published"] = True
        result["scheduled"] = bool(schedule_iso)
        result["scheduled_for"] = schedule_for.isoformat() if schedule_for is not None else None
        result["blogger_response"] = {
            "id": response.get("id"), "url": response.get("url"), "title": response.get("title"),
            "status": response.get("status"),
            "scheduled_for": response.get("scheduled_for"),
            "permalink_status": response.get("permalink_status"),
        }

        img = post.get("feature_image") or {}
        history.append({
            "date_utc": datetime.now(timezone.utc).isoformat(),
            "scheduled_for": schedule_for.isoformat() if schedule_for is not None else "",
            "keyword": keyword,
            "keyword_score": keyword_data.get("score"),
            "demand_tier": keyword_data.get("demand_tier"),
            "keyword_source": keyword_data.get("source"),
            "cluster_key": cluster.get("key"),
            "cluster_name": cluster.get("name"),
            "content_role": cluster.get("content_role"),
            "title": post["title"],
            "url": response.get("url", ""),
            "meta_description": post["meta_description"],
            "labels": post.get("labels", []),
            "permalink": post.get("permalink", ""),
            "content_simhash": post.get("content_simhash", ""),
            "image_source_url": img.get("source_url", ""),
            "image_source_sha256": img.get("source_sha256", ""),
            "image_pageid": img.get("pageid"),
            "feature_image_url": post.get("feature_image_url", ""),
        })
        save_history(history)

    return result


def main():
    parser = argparse.ArgumentParser(description="Modern Kitchen Lab organic topic-cluster Blogger automation")
    parser.add_argument("--publish", action="store_true", help="Publish to Blogger immediately")
    parser.add_argument("--draft", action="store_true", help="When publishing, create a Blogger draft")
    parser.add_argument("--schedule", action="store_true", help="Prepare early and let Blogger publish at the target time")
    parser.add_argument("--target-time", default=DAILY_POST_TIME, help="Local Blogger publish time HH:MM (default from config)")
    args = parser.parse_args()

    target = resolve_publish_target(args.target_time) if args.schedule else None
    if target is not None:
        print(f"Timely mode: prepare now, Blogger will publish at {target.isoformat()}")
    run(
        publish=(args.publish or args.schedule),
        force_draft=True if args.draft else None,
        schedule_for=target,
    )


if __name__ == "__main__":
    main()
