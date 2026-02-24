# Sends a discord ping if job with high match score is found
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_alert(job_title, company, score, reason, link):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    # Use embeds to make Discord message look professional
    data = {
        "content": "**New job found!**",
        "embeds": [{
            "title": f"{job_title} @ {company}",
            "description": f"*Match Score:** {score}/100\n**Reason:** {reason}",
            "url": link,
            "color": 5814783
        }]
    }

    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            print(f"Discord alert sent for {job_title}!")
    except Exception as e:
        print(f"Failed to send Discord alert: {e}")
    