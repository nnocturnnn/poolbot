import sqlite3

def start_db():
    conn = sqlite3.connect('bots.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                chat_id INT PRIMARY KEY,
                locale TEXT,
                info TEXT,
                list_user TEXT);
                """)
    conn.commit()


def insert_db(chat_id,locale="none",info="none",list_user="none"):
    conn = sqlite3.connect('bots.db')
    cur = conn.cursor()
    if locale == "none" and info == "none" and list_user == "none":
        user = (chat_id, locale, info, list_user)
        cur.executemany("INSERT INTO users VALUES(?, ?, ?, ?);", user)
    elif locale != "none":
        sql = """UPDATE ListMembers SET locale = %s WHERE chat_id = %s"""
        cur.execute(sql, (locale, chat_id))
    elif info != "none":
        sql = """UPDATE ListMembers SET info = %s WHERE chat_id = %s"""
        cur.execute(sql, (locale, chat_id))
    elif list_user != "none":
        sql = """UPDATE ListMembers SET list_user = %s WHERE chat_id = %s"""
        cur.execute(sql, (locale, chat_id))
    conn.commit()