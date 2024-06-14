import sqlite3
import os

DB_DIR = 'db_files'
DB_PATH = os.path.join(DB_DIR, 'bot.db')

def initialize_bot_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_stars (
                    user_id INTEGER PRIMARY KEY,
                    star INTEGER
                )''')
    conn.commit()
    conn.close()

def update_star(user_id, star):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO user_stars (user_id, star) VALUES (?, ?)', (user_id, star))
        conn.commit()

def get_star(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT star FROM user_stars WHERE user_id = ?', (user_id,))
        row = c.fetchone()
    return row[0] if row else 1
