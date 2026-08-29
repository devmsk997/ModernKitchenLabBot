from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/blogger"
]

BLOG_ID = "454152404757485701"

creds = Credentials.from_authorized_user_file(
    "token.json",
    SCOPES
)

if creds.expired and creds.refresh_token:
    creds.refresh(Request())

service = build(
    "blogger",
    "v3",
    credentials=creds
)

post = {
    "kind": "blogger#post",
    "title": "Modern Kitchen Lab Bot Test",
    "content": """
<h2>Modern Kitchen Lab Automation Test</h2>

<p>This is a test article created by the new
Modern Kitchen Lab Python automation bot.</p>

<p>If you can see this post inside Blogger Drafts,
the Blogger API connection is working correctly.</p>
"""
}

result = service.posts().insert(
    blogId=BLOG_ID,
    body=post,
    isDraft=True
).execute()

print("")
print("======================================")
print("SUCCESS!")
print("Draft created in Modern Kitchen Lab.")
print("Post ID:", result.get("id"))
print("Title:", result.get("title"))
print("======================================")