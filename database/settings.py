import sqlite3
import os

DB_DIR = 'db_files'
DB_PATH = os.path.join(DB_DIR, 'database.db')

def update_birthday_channel(channel_id):
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO settings (id, birthday_channel_id) VALUES (?, ?)', (1, channel_id))
        conn.commit()

def get_birthday_channel():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT birthday_channel_id FROM settings WHERE id = 1')
        channel_id = c.fetchone()
    return channel_id[0] if channel_id else None
