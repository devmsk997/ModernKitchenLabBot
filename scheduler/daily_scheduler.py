import schedule
import time
import subprocess
from datetime import datetime


def run_blog_bot():

    print("\n======================")
    print("RUNNING BLOG BOT")
    print(datetime.now())
    print("======================")

    subprocess.run(
        [
            "python",
            "blogger/blogger_upload.py"
        ]
    )


schedule.every().day.at("21:00").do(
    run_blog_bot
)


print("===== BLOG SCHEDULER STARTED =====")
print("Daily posting time: 9:00 PM")


while True:

    schedule.run_pending()

    time.sleep(60)