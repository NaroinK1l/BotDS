import sqlite3
import os

DB_DIR = 'db_files'
DB_PATH = os.path.join(DB_DIR, 'levels.db')

def initialize_exp_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_exp (
                    user_id INTEGER PRIMARY KEY,
                    exp INTEGER,
                    level INTEGER DEFAULT 0
                )''')
    conn.commit()
    conn.close()

def update_user_exp(user_id, exp):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO user_exp (user_id, exp) VALUES (?, ?)', (user_id, exp))
        conn.commit()

def update_user_level(user_id, level):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('UPDATE user_exp SET level = ? WHERE user_id = ?', (level, user_id))
        conn.commit()

def get_user_exp(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT exp FROM user_exp WHERE user_id = ?', (user_id,))
        row = c.fetchone()
    return row[0] if row else 0

def get_user_level(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT level FROM user_exp WHERE user_id = ?', (user_id,))
        row = c.fetchone()
    return row[0] if row else 0

def get_all_user_ids():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT user_id FROM user_exp')
        rows = c.fetchall()
    return {row[0] for row in rows}
