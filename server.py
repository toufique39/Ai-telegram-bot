from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

VERIFY_TOKEN = os.getenv("IG_VERIFY_TOKEN", "verify_toufique_ig")
IG_PAGE_TOKEN = os.getenv("IG_PAGE_TOKEN")

@app.get("/")
def root():
    return {"status": "ok", "service": "ai-telegram-bot"}

# Webhook verification (GET)
@app.get("/webhook/instagram")
def verify_webhook(
    hub_mode: str = None,
    hub_challenge: str = None,
    hub_verify_token: str = None,
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)
    return "Verification failed"

# Receive messages (POST)
@app.post("/webhook/instagram")
async def receive_instagram_webhook(request: Request):
    data = await request.json()
    print("INSTAGRAM POST RECEIVED:", data)

    for entry in data.get("entry", []):
        for msg_event in entry.get("messaging", []):
            message = msg_event.get("message")
            sender = msg_event.get("sender", {}).get("id")

            # ignore echo / self messages
            if message and not message.get("is_echo"):
                text = message.get("text", "")
                send_instagram_reply(sender, f"🤖 Auto Reply: তুমি লিখেছো → {text}")

    return {"status": "ok"}

def send_instagram_reply(recipient_id, text):
    url = "https://graph.facebook.com/v19.0/me/messages"
    headers = {
        "Authorization": f"Bearer {IG_PAGE_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }

    r = requests.post(url, headers=headers, json=payload)
    print("REPLY STATUS:", r.status_code, r.text)
