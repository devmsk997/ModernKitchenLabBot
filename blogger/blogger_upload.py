from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from config import (
    BLOGGER_API_SCOPES,
    BLOG_ID,
    MAX_EXISTING_POSTS,
    TOKEN_FILE,
    USE_PERMALINK_WORKAROUND,
)


def get_blogger_service():
    if not TOKEN_FILE.exists():
        raise FileNotFoundError(f"Missing {TOKEN_FILE.name}. Run: python auth.py")

    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), BLOGGER_API_SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

    return build("blogger", "v3", credentials=creds, cache_discovery=False)


def list_existing_posts(limit: int = MAX_EXISTING_POSTS) -> list[dict[str, Any]]:
    service = get_blogger_service()
    posts: list[dict[str, Any]] = []
    page_token = None

    while len(posts) < limit:
        response = (
            service.posts().list(
                blogId=BLOG_ID,
                maxResults=min(100, limit - len(posts)),
                pageToken=page_token,
                fetchBodies=True,
                fetchImages=True,
                status=["LIVE", "DRAFT", "SCHEDULED"],
                view="ADMIN",
            ).execute()
        )
        posts.extend(response.get("items", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            break

    return [{
        "id": p.get("id"),
        "title": p.get("title", ""),
        "url": p.get("url", ""),
        "labels": p.get("labels", []),
        "published": p.get("published", ""),
        "status": p.get("status", ""),
        "content": p.get("content", ""),
        "images": [x.get("url", "") for x in (p.get("images") or []) if isinstance(x, dict) and x.get("url")],
    } for p in posts]


def _insert_post(service, title: str, content: str, labels: list[str], is_draft: bool):
    body = {
        "kind": "blogger#post",
        "title": title,
        "content": content,
        "labels": labels[:20],
    }
    return service.posts().insert(
        blogId=BLOG_ID,
        body=body,
        isDraft=is_draft,
        fetchBody=True,
        fetchImages=True,
    ).execute()


def _url_slug(url: str) -> str:
    path = urlparse(url or "").path.rstrip("/")
    leaf = path.rsplit("/", 1)[-1]
    return leaf[:-5] if leaf.endswith(".html") else leaf


def upload_to_blogger(
    post: dict[str, Any],
    is_draft: bool = False,
    schedule_at: str | None = None,
) -> dict[str, Any]:
    """Create, publish, or schedule a Blogger post.

    ``schedule_at`` is an RFC3339 datetime. When provided, Blogger itself owns the
    final publish time via ``posts.publish(..., publishDate=...)``. This is more
    dependable for exact reader-facing timing than waiting for a cloud runner at the
    exact minute.

    Blogger API v3 has no supported custom-permalink input and no reliable per-post
    Search Description input. For non-draft posts, the optional permalink workaround
    creates a draft using the desired slug as the temporary title, schedules/publishes
    it, then restores the real title.
    """
    service = get_blogger_service()
    title = post["title"].strip()
    content = post["content"].strip()
    labels = post.get("labels", [])
    slug = post.get("permalink", "").strip()

    if is_draft:
        response = _insert_post(service, title, content, labels, True)
        response["permalink_status"] = "draft_or_blogger_default"
        response["scheduled_for"] = None
        return response

    # Schedule through Blogger itself so the post can go live at the requested time
    # even when GitHub Actions started the preparation hours earlier.
    if schedule_at:
        temp_title = slug if (USE_PERMALINK_WORKAROUND and slug) else title
        draft = _insert_post(service, temp_title, content, labels, True)
        post_id = draft["id"]
        scheduled = service.posts().publish(
            blogId=BLOG_ID,
            postId=post_id,
            publishDate=schedule_at,
        ).execute()

        response = scheduled
        if temp_title != title:
            response = service.posts().patch(
                blogId=BLOG_ID,
                postId=post_id,
                body={"title": title},
                fetchBody=True,
                fetchImages=True,
            ).execute()

        actual = _url_slug(response.get("url") or scheduled.get("url") or "")
        if slug and USE_PERMALINK_WORKAROUND:
            response["permalink_status"] = "matched" if actual == slug else f"best_effort_actual:{actual or 'unknown'}"
        else:
            response["permalink_status"] = "blogger_default"
        response["requested_permalink"] = slug
        response["scheduled_for"] = schedule_at
        response["search_description_generated"] = post.get("meta_description", "")
        return response

    if not USE_PERMALINK_WORKAROUND or not slug:
        response = _insert_post(service, title, content, labels, False)
        response["permalink_status"] = "blogger_default"
        response["scheduled_for"] = None
        response["search_description_generated"] = post.get("meta_description", "")
        return response

    # Best-effort custom slug for immediate live publishing.
    draft = _insert_post(service, slug, content, labels, True)
    post_id = draft["id"]
    published = service.posts().publish(blogId=BLOG_ID, postId=post_id).execute()
    response = service.posts().patch(
        blogId=BLOG_ID,
        postId=post_id,
        body={"title": title},
        fetchBody=True,
        fetchImages=True,
    ).execute()

    actual = _url_slug(response.get("url") or published.get("url") or "")
    response["permalink_status"] = "matched" if actual == slug else f"best_effort_actual:{actual or 'unknown'}"
    response["requested_permalink"] = slug
    response["scheduled_for"] = None
    response["search_description_generated"] = post.get("meta_description", "")
    return response


def save_publish_receipt(response: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "id": response.get("id"),
        "title": response.get("title"),
        "url": response.get("url"),
        "published": response.get("published"),
        "status": response.get("status"),
        "scheduled_for": response.get("scheduled_for"),
        "labels": response.get("labels", []),
        "requested_permalink": response.get("requested_permalink"),
        "permalink_status": response.get("permalink_status"),
        "search_description_generated": response.get("search_description_generated"),
        "search_description_api_status": "generated_but_blogger_api_cannot_set_editor_field",
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
