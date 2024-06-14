import sqlite3
import os

DB_DIR = 'db_files'
DB_PATH = os.path.join(DB_DIR, 'bot.db')

def initialize_bot_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS special_points (
                    user_id INTEGER PRIMARY KEY,
                    points INTEGER
                )''')
    conn.commit()
    conn.close()

def update_special_points(user_id, points):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO special_points (user_id, points) VALUES (?, ?)', (user_id, points))
        conn.commit()

def get_special_points(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT points FROM special_points WHERE user_id = ?', (user_id,))
        row = c.fetchone()
    return row[0] if row else 0
