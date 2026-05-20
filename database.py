import sqlite3
from datetime import datetime
import json

def init_db():
    conn = sqlite3.connect("bot_data.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            message TEXT,
            timestamp TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_styles (
            user_id INTEGER PRIMARY KEY,
            style_notes TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS search_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            query TEXT,
            results TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_message(user_id, username, message):
    conn = sqlite3.connect("bot_data.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO messages (user_id, username, message, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user_id, username, message, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_user_history(user_id, limit=10):
    conn = sqlite3.connect("bot_data.db")
    c = conn.cursor()
    c.execute("""
        SELECT message, timestamp FROM messages
        WHERE user_id = ?
        ORDER BY timestamp DESC LIMIT ?
    """, (user_id, limit))
    rows = c.fetchall()
    conn.close()
    return rows

def save_user_style(user_id, style_notes):
    conn = sqlite3.connect("bot_data.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO user_styles (user_id, style_notes)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET style_notes = ?
    """, (user_id, style_notes, style_notes))
    conn.commit()
    conn.close()

def get_user_style(user_id):
    conn = sqlite3.connect("bot_data.db")
    c = conn.cursor()
    c.execute("SELECT style_notes FROM user_styles WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else ""

def save_search_result(user_id, query, results):
    conn = sqlite3.connect("bot_data.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO search_results (user_id, query, results, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user_id, query, json.dumps(results), datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_search_history(user_id, limit=5):
    conn = sqlite3.connect("bot_data.db")
    c = conn.cursor()
    c.execute("""
        SELECT query, results, timestamp FROM search_results
        WHERE user_id = ?
        ORDER BY timestamp DESC LIMIT ?
    """, (user_id, limit))
    rows = c.fetchall()
    conn.close()
    return [(q, json.loads(r), t) for q, r, t in rows]
