from fastapi import FastAPI, Request
import os

app = FastAPI()

VERIFY_TOKEN = os.getenv("IG_VERIFY_TOKEN", "verify_toufique_ig")

@app.get("/")
def root():
    return {"status": "ok", "service": "ai-telegram-bot"}

@app.get("/webhook/instagram")
def verify(
    hub_mode: str = None,
    hub_challenge: str = None,
    hub_verify_token: str = None,
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)
    return {"error": "verification failed"}

@app.post("/webhook/instagram")
async def webhook(request: Request):
    data = await request.json()
    print("IG Webhook:", data)
    return {"status": "received"}
