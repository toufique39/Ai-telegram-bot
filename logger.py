from datetime import datetime

def log_event(user_id: int, event: str):
    with open("bot.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {user_id} | {event}\n")
