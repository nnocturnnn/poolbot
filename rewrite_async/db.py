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


def insert_db(chat_id,locale,info,list_user):
    conn = sqlite3.connect('bots.db')
    cur = conn.cursor()
    user = (chat_id, locale, info, list_user)
    cur.executemany("INSERT INTO users VALUES(?, ?, ?, ?);", user)
    conn.commit()