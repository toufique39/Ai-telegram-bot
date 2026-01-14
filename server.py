from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import os

app = FastAPI()

VERIFY_TOKEN = os.getenv("IG_VERIFY_TOKEN", "verify_toufique_ig")

@app.get("/")
def root():
    return {"status": "ok", "service": "Ai-telegram-bot"}

@app.get("/webhook/instagram")
async def verify_instagram(request: Request):
    params = request.query_params

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)

    return PlainTextResponse("Verification failed", status_code=403)
    @app.post("/webhook/instagram")
async def receive_instagram_webhook(request: Request):
    data = await request.json()
    print("IG EVENT:", data)

    try:
        entry = data["entry"][0]
        messaging = entry["messaging"][0]
        sender_id = messaging["sender"]["id"]
        text = messaging["message"]["text"]

        # এখানে তোমার AI engine কল হবে
        ai_reply = "হ্যালো 😊 আমি এখন কাজ করছি।"

        send_url = f"https://graph.facebook.com/v24.0/me/messages?access_token={IG_TOKEN}"
        payload = {
            "recipient": {"id": sender_id},
            "message": {"text": ai_reply}
        }

        requests.post(send_url, json=payload)

    except Exception as e:
        print("ERROR:", e)

    return {"status": "received"}
