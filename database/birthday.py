import sqlite3
import os

DB_DIR = 'db_files'
DB_PATH = os.path.join(DB_DIR, 'bot.db')

def initialize_birthday_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_birthdays (
                    user_id INTEGER PRIMARY KEY,
                    birthday TEXT
                )''')
    conn.commit()
    conn.close()

def update_birthday(user_id, birthday):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO user_birthdays (user_id, birthday) VALUES (?, ?)', (user_id, birthday))
        conn.commit()

def get_birthday(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT birthday FROM user_birthdays WHERE user_id = ?', (user_id,))
        birthday = c.fetchone()
    return birthday[0] if birthday else None

def get_users_with_birthday(date):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT user_id FROM user_birthdays WHERE strftime("%d-%m", birthday) = ?', (date,))
        rows = c.fetchall()
    return [row[0] for row in rows]
