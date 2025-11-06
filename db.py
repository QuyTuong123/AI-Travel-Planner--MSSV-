import sqlite3

def init_db():
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS history(
        user TEXT, origin TEXT, destination TEXT, plan TEXT)""")
    conn.commit()
    conn.close()

def save_plan(user, origin, destination, plan):
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute("INSERT INTO history VALUES (?, ?, ?, ?)", (user, origin, destination, plan))
    conn.commit()
    conn.close()

def get_history(user):
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute("SELECT * FROM history WHERE user=?", (user,))
    data = c.fetchall()
    conn.close()
    return data
