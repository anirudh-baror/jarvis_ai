import sqlite3

DB_NAME = "memory.db"

def init_db():
    """
    Creates the database and table if they don't already exist.
    Called once when the app starts.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_message(role, message):
    """
    Saves a single message to the database.
    role = 'user' or 'assistant' (who said it).
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conversation_history (role, message) VALUES (?, ?)",
        (role, message)
    )
    conn.commit()
    conn.close()

def get_recent_history(limit=6):
    """
    Returns the most recent 'limit' messages (default: last 6),
    so Gemini has context of the recent conversation.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, message FROM conversation_history ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    # Reverse so messages are in oldest-to-newest order
    return list(reversed(rows))