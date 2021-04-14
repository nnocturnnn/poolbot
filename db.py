import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']

def start_db():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                chat_id BIGINT PRIMARY KEY,
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
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    if locale == "none" and info == "none" and list_user == "none" and \
        date == "none" and price == "none" and private == "none" and mono == "none":
        user = (chat_id, locale, info, list_user, date, price, private, mono)
        cur.execute("INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s, %s, %s);", user)
    elif locale != "none":
        sql = """UPDATE users SET locale = %s WHERE chat_id = %s"""
        cur.execute(sql, (locale , chat_id))
    elif info != "none":
        sql = """UPDATE users SET info = %s WHERE chat_id = %s"""
        cur.execute(sql, (info, chat_id))
    elif date != "none":
        sql = """UPDATE users SET date = %s WHERE chat_id = %s"""
        cur.execute(sql, (date, chat_id))
    elif price != "none":
        sql = """UPDATE users SET price = %s WHERE chat_id = %s"""
        cur.execute(sql, (price, chat_id))
    elif private != "none":
        sql = """UPDATE users SET private = %s WHERE chat_id = %s"""
        cur.execute(sql, (private, chat_id))
    elif mono != "none":
        sql = """UPDATE users SET mono = %s WHERE chat_id = %s"""
        cur.execute(sql, (mono, chat_id))
    elif list_user != "none":
        sql = """UPDATE users SET list_user = %s WHERE chat_id = %s"""
        cur.execute(sql, (list_user, chat_id))
    conn.commit()
    cur.close()
    conn.close()

def get_from_db(chat_id,message):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    if message == "info":
        sql = """SELECT info FROM users WHERE chat_id = %s"""
        cur.execute(sql, (chat_id,))
    elif message == "date":
        sql = """SELECT date FROM users  WHERE chat_id = %s"""
        cur.execute(sql, (chat_id,))
    elif message == "locale":
        sql = """SELECT locale FROM users WHERE chat_id = %s"""
        cur.execute(sql, (chat_id,))
    elif message == "price":
        sql = """SELECT price FROM users WHERE chat_id = %s"""
        cur.execute(sql, (chat_id,))
    elif message == "card_info":
        sql = """SELECT card_info FROM users WHERE chat_id = %s"""
        cur.execute(sql, (chat_id,))
    elif message == "private":
        sql = """SELECT private FROM users WHERE chat_id = %s"""
        cur.execute(sql, (chat_id,))
    elif message == "mono":
        sql = """SELECT mono FROM users WHERE chat_id = %s"""
        cur.execute(sql, (chat_id,))
    elif message == "list_user":
        sql = """SELECT list_user FROM users WHERE chat_id = %s"""
        cur.execute(sql, (chat_id,))
    return cur.fetchone()[0]

