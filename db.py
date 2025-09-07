import sqlite3
import time
DB_NAME = "gamebot.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            balance INTEGER DEFAULT 5000,
            status TEXT DEFAULT 'None',
            chance INTEGER DEFAULT 0,
            last_bonus INTEGER DEFAULT 0,
            hide_top INTEGER DEFAULT 0,
            last_box INTEGER DEFAULT 0
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS promo (
            code TEXT PRIMARY KEY,
            reward INTEGER,
            used_by TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_user(user_id, username=None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cur.fetchone()
    if not user:
        cur.execute("INSERT INTO users (user_id, username) VALUES (?,?)", (user_id, username))
        conn.commit()
        cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        user = cur.fetchone()
    conn.close()
    return user

def update_balance(user_id, diff):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE users SET balance=balance+? WHERE user_id=?", (diff, user_id))
    conn.commit()
    conn.close()

def set_user_chance(user_id, chance):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE users SET chance=? WHERE user_id=?", (chance, user_id))
    conn.commit()
    conn.close()

def set_user_status(user_id, status):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE users SET status=? WHERE user_id=?", (status, user_id))
    conn.commit()
    conn.close()

def reset_bonus_time(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE users SET last_bonus=? WHERE user_id=?", (int(time.time()), user_id))
    conn.commit()
    conn.close()

def reset_box_time(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE users SET last_box=? WHERE user_id=?", (int(time.time()), user_id))
    conn.commit()
    conn.close()

def get_profile(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT username, balance, status, chance FROM users WHERE user_id=?", (user_id,))
    profile = cur.fetchone()
    conn.close()
    return profile

def get_top_users():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT user_id, username, balance FROM users WHERE hide_top=0 ORDER BY balance DESC LIMIT 10")
    top = cur.fetchall()
    conn.close()
    return top

def set_hide_top(user_id, val):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE users SET hide_top=? WHERE user_id=?", (val, user_id))
    conn.commit()
    conn.close()

def get_all_user_ids():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users")
    ids = [row[0] for row in cur.fetchall()]
    conn.close()
    return ids

def create_promo(code, reward):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO promo (code, reward, used_by) VALUES (?, ?, '')", (code, reward))
    conn.commit()
    conn.close()

def use_promo(user_id, code):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT reward, used_by FROM promo WHERE code=?", (code,))
    res = cur.fetchone()
    if not res:
        conn.close()
        return None, "❌ Промокод не найден."
    reward, used_by = res
    if used_by and str(user_id) in used_by.split(','):
        conn.close()
        return None, "❌ Вы уже активировали этот промокод."
    # Записать использование
    new_used = used_by + ("," if used_by else "") + str(user_id)
    cur.execute("UPDATE promo SET used_by=? WHERE code=?", (new_used, code))
    update_balance(user_id, reward)
    conn.commit()
    conn.close()
    return reward, f"🎟 Промокод активирован! Вы получили {reward} GG."

def get_promo_logs():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT code, reward, used_by FROM promo")
    logs = cur.fetchall()
    conn.close()
    return logs
