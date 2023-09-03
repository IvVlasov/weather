import sqlite3
from settings import DB_PATH


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def create_con():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = dict_factory
    return con


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


def get_or_create_yandex_history(city, lon, lat, dt):
    con = create_con()
    cursor = con.cursor()
    lon, lat = round(lon, 1), round(lat, 1)
    query = 'SELECT stat_id FROM yandex_history WHERE city=? AND lon=? AND lat=? AND dt = ?'
    cursor.execute(query, (city, lon, lat, dt))
    row_id = cursor.fetchone()
    if not row_id:
        query = 'INSERT INTO yandex_history (city, lon, lat, dt) VALUES (?, ?, ?, ?) RETURNING stat_id'
        cursor.execute(query, (city, lon, lat, dt))
        row_id = cursor.fetchone()
    con.commit()
    con.close()
    return row_id


def create_yandex_history_detail(stat_id, part, temp_avg, wind_speed, wind_dir, pressure_mm, humidity, prec_type):
    con = create_con()
    cursor = con.cursor()
    
    query = 'INSERT INTO yandex_history_detail \
        (stat_id, part, temp_avg, wind_speed, wind_dir, pressure_mm, humidity, prec_type) \
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
    cursor.execute(query, (stat_id, part, temp_avg, wind_speed, wind_dir, pressure_mm, humidity, prec_type))
    con.commit()
    con.close()


def get_yandex_history_weather(lon, lat, dt):
    con = create_con()
    cursor = con.cursor()
    query = 'select * from yandex_history join yandex_history_detail using(stat_id) WHERE lon=? AND lat=? AND dt=?'
    
    lon, lat = round(lon, 1), round(lat, 1)
    dt = dt.strftime('%Y-%m-%d')
    
    cursor.execute(query, (lon, lat, dt))
    res = cursor.fetchone()
    print(res)


create_sql()
from datetime import datetime

get_or_create_yandex_history('hello', 12.31, 123.522,  datetime.today())
# create_yandex_history_detail(1, 'day', 10, 31, 31, 31, 'nw', 13)
# get_yandex_history_weather(12.31, 123.522, datetime.today())