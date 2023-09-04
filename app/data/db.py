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
    query = 'SELECT lon, lat, city FROM user WHERE chat_id=?'
    cursor.execute(query, (chat_id, ))
    row = cursor.fetchone()
    con.close()
    return row['lon'], row['lat'], row['city']


def get_user_city(chat_id):
    con = create_con()
    cursor = con.cursor()
    query = 'SELECT lon, lat FROM user WHERE chat_id=?'
    cursor.execute(query, (chat_id, ))
    row = cursor.fetchone()
    con.close()
    return row['lon'], row['lat']


''' Yandex '''


def get_or_create_weather_history(city, lon, lat, dt):
    con = create_con()
    cursor = con.cursor()
    dt = dt.strftime('%Y-%m-%d')
    lon, lat = round(lon, 3), round(lat, 3)

    query = 'SELECT * FROM weather_history WHERE lon=? AND lat=? AND dt = ?'
    cursor.execute(query, (lon, lat, dt))
    row = cursor.fetchone()
    if not row:
        query = 'INSERT INTO weather_history (city, lon, lat, dt) VALUES (?, ?, ?, ?) RETURNING *'
        cursor.execute(query, (city, lon, lat, dt))
        row = cursor.fetchone()
    con.commit()
    con.close()
    return row


def create_weather_history_detail(stat_id, source, part, temp_avg, wind_speed, wind_dir,
                                  pressure_mm, humidity, prec_type):
    con = create_con()
    cursor = con.cursor()

    query = 'SELECT * FROM weather_history_detail\
        WHERE stat_id=? AND source=? AND part=?'
    cursor.execute(query, (stat_id, source, part))
    row = cursor.fetchone()
    if row:
        return

    query = 'INSERT INTO weather_history_detail \
        (stat_id, source, part, temp_avg, wind_speed, wind_dir, pressure_mm, humidity, prec_type) \
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
    cursor.execute(query, (stat_id, source, part, temp_avg, wind_speed, wind_dir, pressure_mm, humidity, prec_type))
    con.commit()
    con.close()


def get_weather_detail(stat_id, source):
    con = create_con()
    cursor = con.cursor()

    query = 'select * from weather_history_detail whd \
        join weather_history wh using(stat_id) \
        WHERE stat_id=? AND whd.source=?'

    cursor.execute(query, (stat_id, source))
    res = cursor.fetchall()
    return res
    print(res)


create_sql()
