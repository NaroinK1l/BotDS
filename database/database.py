import sqlite3
import os

DB_DIR = 'db_files'
DB_PATH = os.path.join(DB_DIR, 'bot.db')

def initialize_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS excluded_channels (
                    id INTEGER PRIMARY KEY
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS excluded_roles (
                    id INTEGER PRIMARY KEY
                )''')
    conn.commit()
    conn.close()

def add_excluded_channel(channel_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO excluded_channels (id) VALUES (?)', (channel_id,))
        conn.commit()

def remove_excluded_channel(channel_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('DELETE FROM excluded_channels WHERE id = ?', (channel_id,))
        conn.commit()

def get_excluded_channels():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT id FROM excluded_channels')
        rows = c.fetchall()
    return {row[0] for row in rows}

def add_excluded_role(role_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO excluded_roles (id) VALUES (?)', (role_id,))
        conn.commit()

def remove_excluded_role(role_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('DELETE FROM excluded_roles WHERE id = ?', (role_id,))
        conn.commit()

def get_excluded_roles():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT id FROM excluded_roles')
        rows = c.fetchall()
    return {row[0] for row in rows}
