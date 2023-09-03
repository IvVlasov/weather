
CREATE TABLE IF NOT EXISTS user (
    chat_id INTEGER PRIMARY KEY,
    lon TEXT default NULL,
    lat TEXT default NULL,
    city TEXT default NULL
);
CREATE TABLE IF NOT EXISTS yandex_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    lon REAL,
    lat REAL,
    dt TEXT
);
CREATE TABLE IF NOT EXISTS yandex_history_detail (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stat_id INTEGER,
    part TEXT, -- day/morning/night/evening
    temp_avg INTEGER,
    wind_speed INTEGER,
    wind_dir TEXT, -- nw/n/ne/e/se/s/sw/w/c
    pressure_mm INTEGER,
    humidity INTEGER,
    prec_type INTEGER, -- 0/1/2/3
    FOREIGN KEY (stat_id)  REFERENCES yandex_history (id)
);