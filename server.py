from fastapi import FastAPI, Request
import os
import requests

app = FastAPI()

PAGE_TOKEN = os.getenv("FB_PAGE_TOKEN")
VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN")

@app.get("/webhook/facebook")
def verify_webhook(request: Request):
    params = request.query_params
    if (
        params.get("hub.mode") == "subscribe"
        and params.get("hub.verify_token") == VERIFY_TOKEN
    ):
        return int(params.get("hub.challenge"))
    return "Verification failed"

@app.post("/webhook/facebook")
async def receive_message(request: Request):
    data = await request.json()
    for entry in data.get("entry", []):
        for msg in entry.get("messaging", []):
            sender_id = msg["sender"]["id"]
            if "text" in msg.get("message", {}):
                send_reply(sender_id, "Hello! 👋 This is auto reply.")
    return {"status": "ok"}

def send_reply(psid, text):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_TOKEN}"
    payload = {
        "recipient": {"id": psid},
        "message": {"text": text}
    }
    requests.post(url, json=payload)
