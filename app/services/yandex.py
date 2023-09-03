import requests
from settings import WEATHER_TOKEN
from services import db


def get_weather(lon, lat, date):
    date_stroke = date.strftime('%Y-%m-%d')

    # Поиск даты в базе данных, вдруг она уже есть на эти координаты

    forecasts = get_weather_data(lat, lon)
    for forecast in forecasts:
        if forecast['date'] == date_stroke:
            weather_stroke = _get_forecast_weather_stroke(forecast)
            print(weather_stroke)


def get_weather_data(lat, lon):
    url = 'https://api.weather.yandex.ru/v2/forecast?lat=%s&lon=%s&lang=ru_RU&limit=3&hours=false&extra=true'
    url = url % (str(lat), str(lon))
    header = {"X-Yandex-API-Key": WEATHER_TOKEN}
    r = requests.get(url, headers=header)
    print(r.json())
    return r.json()['forecasts']


def _get_forecast_weather_stroke(forecast):
    result = 'Погода:\n\nУтром:%s\n Днём: %s\nВечером: %s\nНочью: %s'
    parts = forecast['parts']
    morning = _set_sub_stroke(parts['morning'])
    day = _set_sub_stroke(parts['day'])
    evening = _set_sub_stroke(parts['evening'])
    night = _set_sub_stroke(parts['night'])
    return result % (morning, day, evening, night)


def _get_precipitation(prec_type):
    if prec_type == 0:
        return 'Без осадков'
    if prec_type == 1:
        return 'Дождь'
    if prec_type == 2:
        return 'Дождь со снегом'
    if prec_type == 3:
        return 'Снег'


def _set_sub_stroke(part):
    sub_stroke = '---\nТемпература: %s. Осадки: %s. Скорость ветра: %s м/с\n'
    result = sub_stroke % (part['temp_avg'], _get_precipitation(part['prec_type']), part['wind_speed'])
    return result


lon = 39.83023
lat = 57.583337

from datetime import datetime, timedelta
# get_weather(lon, lat, datetime.today() + timedelta(days=1))
