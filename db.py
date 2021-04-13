import sqlite3

def start_db():
    conn = sqlite3.connect('bots.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                chat_id INT PRIMARY KEY,
                locale TEXT,
                info TEXT,
                list_user TEXT,
                date TEXT,
                price TEXT,
                private TEXT,
                mono TEXT);
                """)
    conn.commit()


def insert_db(chat_id,locale="none",info="none",list_user="none",
                date="none",price="none",private="none",mono="none"):
    conn = sqlite3.connect('bots.db')
    cur = conn.cursor()
    if locale == "none" and info == "none" and list_user == "none" and \
        date == "none" and price == "none" and private == "none" and mono == "none":
        user = (chat_id, locale, info, list_user, date, price, private, mono)
        cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?);", user)
    elif locale != "none":
        sql = """UPDATE users SET locale = ? WHERE chat_id = ?"""
        cur.execute(sql, (locale , chat_id))
    elif info != "none":
        sql = """UPDATE users SET info = ? WHERE chat_id = ?"""
        cur.execute(sql, (info, chat_id))
    elif date != "none":
        sql = """UPDATE users SET date = ? WHERE chat_id = ?"""
        cur.execute(sql, (date, chat_id))
    elif price != "none":
        sql = """UPDATE users SET price = ? WHERE chat_id = ?"""
        cur.execute(sql, (price, chat_id))
    elif private != "none":
        sql = """UPDATE users SET private = ? WHERE chat_id = ?"""
        cur.execute(sql, (private, chat_id))
    elif mono != "none":
        sql = """UPDATE users SET mono = ? WHERE chat_id = ?"""
        cur.execute(sql, (mono, chat_id))
    elif list_user != "none":
        sql = """UPDATE users SET list_user = ? WHERE chat_id = ?"""
        cur.execute(sql, (list_user, chat_id))
    conn.commit()

def get_from_db(chat_id,message):
    conn = sqlite3.connect('bots.db')
    cur = conn.cursor()
    if message == "info":
        sql = """SELECT info FROM users WHERE chat_id = ?"""
        cur.execute(sql, (chat_id,))
    elif message == "date":
        sql = """SELECT date FROM users  WHERE chat_id = ?"""
        cur.execute(sql, (chat_id,))
    elif message == "locale":
        sql = """SELECT locale FROM users WHERE chat_id = ?"""
        cur.execute(sql, (chat_id,))
    elif message == "price":
        sql = """SELECT price FROM users WHERE chat_id = ?"""
        cur.execute(sql, (chat_id,))
    elif message == "card_info":
        sql = """SELECT card_info FROM users WHERE chat_id = ?"""
        cur.execute(sql, (chat_id,))
    elif message == "private":
        sql = """SELECT private FROM users WHERE chat_id = ?"""
        cur.execute(sql, (chat_id,))
    elif message == "mono":
        sql = """SELECT mono FROM users WHERE chat_id = ?"""
        cur.execute(sql, (chat_id,))
    elif message == "list_user":
        sql = """SELECT list_user FROM users WHERE chat_id = ?"""
        cur.execute(sql, (chat_id,))
    return cur.fetchone()[0]
