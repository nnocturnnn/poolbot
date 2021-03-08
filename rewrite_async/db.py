import sqlite3

def start_db():
    conn = sqlite3.connect('bots.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                chat_id INT PRIMARY KEY,
                locale TEXT,
                info TEXT,
                list_user TEXT
                date TEXT
                price TEXT
                card_info TEXT);
                """)
    conn.commit()


def insert_db(chat_id,locale="none",info="none",list_user="none",
                date="none",price="none",card_info="none"):
    conn = sqlite3.connect('bots.db')
    cur = conn.cursor()
    if locale == "none" and info == "none" and list_user == "none" and \
        date == "none" and price == "none" and card_info == "none":
        user = (chat_id, locale, info, list_user, date, price, card_info)
        cur.executemany("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?);", user)
    elif locale != "none":
        sql = """UPDATE ListMembers SET locale = %s WHERE chat_id = %s"""
        cur.execute(sql, (locale, chat_id))
    elif info != "none":
        sql = """UPDATE ListMembers SET info = %s WHERE chat_id = %s"""
        cur.execute(sql, (locale, chat_id))
    elif list_user != "none":
        sql = """UPDATE ListMembers SET list_user = %s WHERE chat_id = %s"""
        cur.execute(sql, (locale, chat_id))
    elif date != "none":
        sql = """UPDATE ListMembers SET date = %s WHERE chat_id = %s"""
        cur.execute(sql, (locale, chat_id))
    elif price != "none":
        sql = """UPDATE ListMembers SET price = %s WHERE chat_id = %s"""
        cur.execute(sql, (locale, chat_id))
    elif card_info != "none":
        sql = """UPDATE ListMembers SET card_info = %s WHERE chat_id = %s"""
        cur.execute(sql, (locale, chat_id))
    conn.commit()

def get_from_db(chat_id,message):
    conn = sqlite3.connect('bots.db')
    cur = conn.cursor()
    if message == "info":
        sql = """SELECT info WHERE chat_id = %s"""
        cur.execute(sql, (chat_id))
    elif message == "date":
        sql = """SELECT date WHERE chat_id = %s"""
        cur.execute(sql, (chat_id))
    elif message == "locale":
        sql = """SELECT locale WHERE chat_id = %s"""
        cur.execute(sql, (chat_id))
    elif message == "price":
        sql = """SELECT price WHERE chat_id = %s"""
        cur.execute(sql, (chat_id))
    elif message == "card_info":
        sql = """SELECT card_info WHERE chat_id = %s"""
        cur.execute(sql, (chat_id))
    elif message == "list_user":
        sql = """SELECT list_user WHERE chat_id = %s"""
        cur.execute(sql, (chat_id))
    return "value"