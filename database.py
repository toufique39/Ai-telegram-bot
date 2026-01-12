import sqlite3

DB_NAME = "memory.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Messages table (full conversation history)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        role TEXT,
        content TEXT
    )
    """)

    # Summary table (long-term memory)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS summaries (
        user_id INTEGER PRIMARY KEY,
        summary TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_message(user_id: int, role: str, content: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)",
        (user_id, role, content)
    )

    conn.commit()
    conn.close()


def get_last_messages(user_id: int, limit: int = 10):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM messages
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT ?
        """,
        (user_id, limit)
    )

    rows = cursor.fetchall()
    conn.close()

    # return oldest → newest
    return rows[::-1]


def save_summary(user_id: int, summary: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO summaries (user_id, summary)
    VALUES (?, ?)
    ON CONFLICT(user_id)
    DO UPDATE SET summary=excluded.summary
    """, (user_id, summary))

    conn.commit()
    conn.close()


def get_summary(user_id: int) -> str:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT summary FROM summaries WHERE user_id=?",
        (user_id,)
    )

    row = cursor.fetchone()
    conn.close()

    return row[0] if row else ""


def clear_user_memory(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM messages WHERE user_id=?", (user_id,))
    cursor.execute("DELETE FROM summaries WHERE user_id=?", (user_id,))

    conn.commit()
    conn.close()
