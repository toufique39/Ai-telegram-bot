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
