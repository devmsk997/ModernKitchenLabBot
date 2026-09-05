from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# ---------------- Blogger / auth ----------------
BLOG_ID = os.getenv("BLOG_ID", "454152404757485701").strip()
BLOGGER_API_SCOPES = ["https://www.googleapis.com/auth/blogger"]
CREDENTIALS_FILE = Path(os.getenv("BLOGGER_CREDENTIALS_FILE", BASE_DIR / "credentials.json"))
TOKEN_FILE = Path(os.getenv("BLOGGER_TOKEN_FILE", BASE_DIR / "token.json"))

# ---------------- Gemini ----------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_TEXT_MODEL = os.getenv("GEMINI_TEXT_MODEL", "gemini-3.5-flash-lite").strip()
GEMINI_TEXT_FALLBACK_MODELS = [
    x.strip()
    for x in os.getenv("GEMINI_TEXT_FALLBACK_MODELS", "gemini-3.1-flash-lite,gemini-3.5-flash,gemini-3.6-flash,gemini-3.7-flash").split(",")
    if x.strip()
]
ENABLE_GEMINI_GROUNDING = os.getenv("ENABLE_GEMINI_GROUNDING", "false").lower() == "true"

# ---------------- Site / audience ----------------
SITE_NAME = os.getenv("SITE_NAME", "Modern Kitchen Lab").strip()
SITE_LANGUAGE = os.getenv("SITE_LANGUAGE", "English (US)").strip()
TARGET_GEO = os.getenv("TARGET_GEO", "US").strip().upper()
TARGET_AUDIENCE = os.getenv(
    "TARGET_AUDIENCE",
    "US homeowners, renters, apartment dwellers, and everyday cooks who want a more functional modern kitchen",
).strip()

# The bot only researches inside this niche. Change these only if the site niche changes.
NICHE_SEEDS = [
    x.strip()
    for x in os.getenv(
        "NICHE_SEEDS",
        "kitchen organization,kitchen storage,small kitchen ideas,pantry organization,"
        "cabinet organization,drawer organization,under sink storage,kitchen layout,"
        "kitchen cleaning,meal prep organization,kitchen gadgets,cookware organization",
    ).split(",")
    if x.strip()
]

# Stable Blogger categories/labels. The cluster engine maps every article to these instead of creating label spam.
BLOGGER_LABEL_TAXONOMY = [
    x.strip()
    for x in os.getenv(
        "BLOGGER_LABEL_TAXONOMY",
        "Kitchen Organization,Storage Solutions,Small Kitchen Ideas,Pantry Organization,"
        "Cabinet Organization,Kitchen Layout,Kitchen Cleaning,Meal Prep,Kitchen Gadgets,"
        "Cookware,Home Improvement",
    ).split(",")
    if x.strip()
]
MAX_BLOGGER_LABELS = int(os.getenv("MAX_BLOGGER_LABELS", "3"))

# ---------------- Organic SEO / editorial quality ----------------
ENABLE_TRENDS = os.getenv("ENABLE_TRENDS", "true").lower() == "true"
# Keyword opportunity filters. In free mode these are transparent proxies, not paid-tool metrics.
KEYWORD_MIN_WORDS = int(os.getenv("KEYWORD_MIN_WORDS", "4"))
KEYWORD_MAX_WORDS = int(os.getenv("KEYWORD_MAX_WORDS", "10"))
KEYWORD_MIN_DEMAND_PROXY = float(os.getenv("KEYWORD_MIN_DEMAND_PROXY", "50"))
KEYWORD_MAX_COMPETITION_PROXY = float(os.getenv("KEYWORD_MAX_COMPETITION_PROXY", "55"))
MIN_ARTICLE_WORDS = int(os.getenv("MIN_ARTICLE_WORDS", "1500"))
MAX_ARTICLE_WORDS = int(os.getenv("MAX_ARTICLE_WORDS", "2400"))
QUALITY_MIN_WORDS = int(os.getenv("QUALITY_MIN_WORDS", "1200"))
QUALITY_MIN_H2 = int(os.getenv("QUALITY_MIN_H2", "6"))
QUALITY_REQUIRE_H3 = os.getenv("QUALITY_REQUIRE_H3", "true").lower() == "true"
MAX_CONTENT_ATTEMPTS = int(os.getenv("MAX_CONTENT_ATTEMPTS", "3"))
MIN_INTERNAL_LINKS = int(os.getenv("MIN_INTERNAL_LINKS", "2"))
MAX_INTERNAL_LINKS = int(os.getenv("MAX_INTERNAL_LINKS", "4"))
MAX_AUTHORITY_LINKS = int(os.getenv("MAX_AUTHORITY_LINKS", "2"))
ADD_AUTOMATION_DISCLOSURE = os.getenv("ADD_AUTOMATION_DISCLOSURE", "false").lower() == "true"

# ---------------- Images ----------------
REQUIRE_FEATURE_IMAGE = os.getenv("REQUIRE_FEATURE_IMAGE", "true").lower() == "true"
FEATURE_IMAGE_PROVIDER = os.getenv("FEATURE_IMAGE_PROVIDER", "aihorde").strip().lower()
WIKIMEDIA_ALLOW_CC_BY_SA = os.getenv("WIKIMEDIA_ALLOW_CC_BY_SA", "true").lower() == "true"
WIKIMEDIA_SEARCH_SUFFIX = os.getenv("WIKIMEDIA_SEARCH_SUFFIX", "home kitchen interior").strip()
IMAGE_DIR = BASE_DIR / os.getenv("IMAGE_DIR", "public_images")
IMAGE_PUBLIC_BASE_URL = os.getenv("IMAGE_PUBLIC_BASE_URL", "").rstrip("/")
AUTO_GIT_PUSH_IMAGES = os.getenv("AUTO_GIT_PUSH_IMAGES", "false").lower() == "true"
GITHUB_IMAGE_OWNER = os.getenv("GITHUB_IMAGE_OWNER", "").strip()
GITHUB_IMAGE_REPO = os.getenv("GITHUB_IMAGE_REPO", "modern-kitchen-blog-images").strip()
GITHUB_IMAGE_TOKEN = os.getenv("GITHUB_IMAGE_TOKEN", "").strip()

# Free AI feature images via AI Horde. The official anonymous key needs no signup,
# but it has the lowest queue priority. A personal AI Horde key can be supplied later.
AI_HORDE_API_KEY = os.getenv("AI_HORDE_API_KEY", "0000000000").strip() or "0000000000"
AI_HORDE_MAX_ATTEMPTS = int(os.getenv("AI_HORDE_MAX_ATTEMPTS", "3"))
AI_HORDE_MAX_WAIT_SECONDS = int(os.getenv("AI_HORDE_MAX_WAIT_SECONDS", "600"))
AI_HORDE_POLL_SECONDS = int(os.getenv("AI_HORDE_POLL_SECONDS", "10"))
AI_HORDE_WIDTH = int(os.getenv("AI_HORDE_WIDTH", "768"))
AI_HORDE_HEIGHT = int(os.getenv("AI_HORDE_HEIGHT", "448"))
AI_HORDE_STEPS = int(os.getenv("AI_HORDE_STEPS", "20"))
TIMELY_IMAGE_FALLBACK = os.getenv("TIMELY_IMAGE_FALLBACK", "true").lower() == "true"


# ---------------- Publishing ----------------
POST_AS_DRAFT = os.getenv("POST_AS_DRAFT", "false").lower() == "true"
USE_PERMALINK_WORKAROUND = os.getenv("USE_PERMALINK_WORKAROUND", "true").lower() == "true"
AFFILIATE_MODE = os.getenv("AFFILIATE_MODE", "false").lower() == "true"
MAX_EXISTING_POSTS = int(os.getenv("MAX_EXISTING_POSTS", "800"))

# ---------------- State / schedule ----------------
HISTORY_FILE = BASE_DIR / "data" / "history.json"
PREVIEW_DIR = BASE_DIR / "data" / "previews"
DAILY_POST_TIME = os.getenv("DAILY_POST_TIME", "21:00").strip()
TIMEZONE_NAME = os.getenv("TIMEZONE_NAME", "Asia/Dhaka").strip()
SCHEDULE_AHEAD = os.getenv("SCHEDULE_AHEAD", "true").lower() == "true"
