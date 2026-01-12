from ai_engine import ask_ai
from database import get_last_messages, save_summary

def summarize_conversation(user_id: int):
    messages = get_last_messages(user_id, limit=20)

    if not messages:
        return

    history_text = ""
    for role, content in messages:
        history_text += f"{role}: {content}\n"

    prompt = f"""
Summarize the following conversation briefly.
Keep important facts, preferences, and goals.

Conversation:
{history_text}
"""

    summary = ask_ai(prompt)
    save_summary(user_id, summary)
