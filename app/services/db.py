import sqlite3
from settings import DB_PATH


def create_con():
    return sqlite3.connect(DB_PATH)


def create_sql():
    # Создаём таблицы базы
    con = create_con()
    with open('data/create.sql', 'r') as sql_file:
        create_sql = sql_file.read()
    cursor = con.cursor()
    cursor.executescript(create_sql)
    con.commit()
    con.close()


''' User '''


def create_user(chat_id):
    con = create_con()
    cursor = con.cursor()
    query = 'INSERT OR IGNORE INTO user (chat_id) VALUES (?)'
    cursor.execute(query, (chat_id, ))
    con.commit()
    con.close()


def set_user_coords(chat_id, lon, lat, city):
    con = create_con()
    cursor = con.cursor()
    query = 'UPDATE user SET lon=?, lat=?, city=? WHERE chat_id=?'
    cursor.execute(query, (lon, lat, city, chat_id))
    con.commit()
    con.close()


def get_user_coords(chat_id):
    con = create_con()
    cursor = con.cursor()
    query = 'SELECT lon, lat FROM user WHERE chat_id=?'
    cursor.execute(query, (chat_id, ))
    row = cursor.fetchone()
    con.close()
    return row[0], row[1]


''' Yandex '''


def create_yandex_history(chat_id):
    con = create_con()
    cursor = con.cursor()
    query = 'INSERT OR IGNORE INTO yandex_history (city, lon, lat, weather, dt) VALUES (?, ?, ?, ?, ?)'
    cursor.execute(query, (chat_id, ))
    con.commit()
    con.close()


create_sql()
