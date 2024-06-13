import sqlite3

def initialize_db():
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_exp (
                    user_id INTEGER PRIMARY KEY,
                    exp INTEGER,
                    level INTEGER DEFAULT 0,
                    birthday TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS excluded_channels (
                    id INTEGER PRIMARY KEY
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS excluded_roles (
                    id INTEGER PRIMARY KEY
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS special_points (
                    user_id INTEGER PRIMARY KEY,
                    points INTEGER
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_stars (
                    user_id INTEGER PRIMARY KEY,
                    star INTEGER
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY,
                    birthday_channel_id INTEGER
                )''')

    # Проверка и добавление недостающего столбца level
    c.execute("PRAGMA table_info(user_exp)")
    columns = [column[1] for column in c.fetchall()]
    if 'level' not in columns:
        c.execute("ALTER TABLE user_exp ADD COLUMN level INTEGER DEFAULT 0")

    conn.commit()
    conn.close()

def add_excluded_channel(channel_id):
    with sqlite3.connect('bot.db') as conn:
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO excluded_channels (id) VALUES (?)', (channel_id,))
        conn.commit()

def remove_excluded_channel(channel_id):
    with sqlite3.connect('bot.db') as conn:
        c = conn.cursor()
        c.execute('DELETE FROM excluded_channels WHERE id = ?', (channel_id,))
        conn.commit()

def get_excluded_channels():
    with sqlite3.connect('bot.db') as conn:
        c = conn.cursor()
        c.execute('SELECT id FROM excluded_channels')
        rows = c.fetchall()
    return {row[0] for row in rows}

def add_excluded_role(role_id):
    with sqlite3.connect('bot.db') as conn:
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO excluded_roles (id) VALUES (?)', (role_id,))
        conn.commit()

def remove_excluded_role(role_id):
    with sqlite3.connect('bot.db') as conn:
        c = conn.cursor()
        c.execute('DELETE FROM excluded_roles WHERE id = ?', (role_id,))
        conn.commit()

def get_excluded_roles():
    with sqlite3.connect('bot.db') as conn:
        c = conn.cursor()
        c.execute('SELECT id FROM excluded_roles')
        rows = c.fetchall()
    return {row[0] for row in rows}

def update_special_points(user_id, points):
    with sqlite3.connect('bot.db') as conn:
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO special_points (user_id, points) VALUES (?, ?)', (user_id, points))
        conn.commit()

def get_special_points(user_id):
    with sqlite3.connect('bot.db') as conn:
        c = conn.cursor()
        c.execute('SELECT points FROM special_points WHERE user_id = ?', (user_id,))
        row = c.fetchone()
    return row[0] if row else 0

def update_star(user_id, star):
    with sqlite3.connect('bot.db') as conn:
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO user_stars (user_id, star) VALUES (?, ?)', (user_id, star))
        conn.commit()

def get_star(user_id):
    with sqlite3.connect('bot.db') as conn:
        c = conn.cursor()
        c.execute('SELECT star FROM user_stars WHERE user_id = ?', (user_id,))
        row = c.fetchone()
    return row[0] if row else 1

def update_user_exp(user_id, exp):
    with sqlite3.connect('bot.db') as conn:
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO user_exp (user_id, exp) VALUES (?, ?)', (user_id, exp))
        conn.commit()

def update_user_level(user_id, level):
    with sqlite3.connect('bot.db') as conn:
        c = conn.cursor()
        c.execute('UPDATE user_exp SET level = ? WHERE user_id = ?', (level, user_id))
        conn.commit()

def get_user_exp(user_id):
    with sqlite3.connect('bot.db') as conn:
        c = conn.cursor()
        c.execute('SELECT exp FROM user_exp WHERE user_id = ?', (user_id,))
        row = c.fetchone()
    return row[0] if row else 0

def get_user_level(user_id):
    with sqlite3.connect('bot.db') as conn:
        c = conn.cursor()
        c.execute('SELECT level FROM user_exp WHERE user_id = ?', (user_id,))
        row = c.fetchone()
    return row[0] if row else 0

def get_all_user_ids():
    with sqlite3.connect('bot.db') as conn:
        c = conn.cursor()
        c.execute('SELECT user_id FROM user_exp')
        rows = c.fetchall()
    return {row[0] for row in rows}

def update_birthday(user_id, birthday):
    with sqlite3.connect('bot.db') as conn:
        c = conn.cursor()
        c.execute('UPDATE user_exp SET birthday = ? WHERE user_id = ?', (birthday, user_id))
        conn.commit()

def get_birthday(user_id):
    with sqlite3.connect('bot.db') as conn:
        c = conn.cursor()
        c.execute('SELECT birthday FROM user_exp WHERE user_id = ?', (user_id,))
        birthday = c.fetchone()
    conn.close()
    return birthday[0] if birthday else None

def update_birthday_channel(channel_id):
    with sqlite3.connect('bot.db') as conn:
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO settings (id, birthday_channel_id) VALUES (?, ?)', (1, channel_id))
        conn.commit()

def get_birthday_channel():
    with sqlite3.connect('bot.db') as conn:
        c = conn.cursor()
        c.execute('SELECT birthday_channel_id FROM settings WHERE id = 1')
        channel_id = c.fetchone()
    return channel_id[0] if channel_id else None
