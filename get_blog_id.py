from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/blogger"
]

creds = Credentials.from_authorized_user_file(
    "token.json",
    SCOPES
)

service = build(
    "blogger",
    "v3",
    credentials=creds
)

blogs = service.blogs().listByUser(
    userId="self"
).execute()

print("")
print("========== YOUR BLOGS ==========")

for blog in blogs.get("items", []):
    print("")
    print("Blog Name :", blog.get("name"))
    print("Blog ID   :", blog.get("id"))
    print("Blog URL  :", blog.get("url"))
    print("--------------------------------")