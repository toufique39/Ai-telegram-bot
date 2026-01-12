import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from safety import is_safe
from ai_engine import ask_ai
from logger import log_event
from database import init_db
from database import (
    init_db,
    save_message,
    get_last_messages,
    save_summary,
    get_summary,
    clear_user_memory
)
from memory_control import summarize_conversation

API_TOKEN = "8400788230:AAF8QTT9a03MbVRjVbCOHOeiB08L4OdJWlw"

# Dispatcher must be global
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "হ্যালো 👋\n"
        "আমি Toufique-এর AI Agent 🤖\n\n"
        "আমি তোমার সাথে কথা মনে রাখতে পারি,\n"
        "আর দরকার হলে ভুলেও যেতে পারি 🙂\n\n"
        "কমান্ড:\n"
        "• মনে রেখো\n"
        "• ভুলে যাও"
    )


@dp.message()
async def smart_reply(message: types.Message):
    await message.answer("Iam working on it...")
    user_id = message.from_user.id
    user_text = message.text
    
    # ---------- SAVE USER MESSAGE ----------
    save_message(user_id, "user", user_text)

    
    # ---------- SAFETY CHECK ----------
    if not is_safe(user_text):
        warning_reply = "দুঃখিত 😔 আপনার বাক্যটি নিষিদ্ধ বিষয় ধরে নেয়।"
        await message.answer(warning_reply)
        return

    # ---------- LOAD MEMORY ----------
    history = get_last_messages(user_id, limit=6)
    summary = get_summary(user_id)

    history_text = ""
    for role, content in history:
        history_text += f"{role}: {content}\n"

    # ---------- AI PROMPT ----------
    ai_prompt = f"""
You are a helpful AI assistant.

User memory summary:
{summary}

Conversation history:
{history_text}

User message:
{user_text}

Respond to the user message appropriately.
"""
    
    

    # ---------- AI REPLY ----------
    try:
        ai_reply = ask_ai(user_text)
        save_message(user_id, "assistant", ai_reply)
        await message.answer(ai_reply)
        log_event(user_id, f"AI reply: {ai_reply}")

    
    except Exception as e:
          await message.answer(f"AI ERROR: {e}")
          print("AI ERROR:", e)
    
    


async def main():
    # Initialize database once
    init_db()

    bot = Bot(token=API_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
