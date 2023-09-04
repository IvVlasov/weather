from data import db
from services.modules import yandex, gismeteo
from datetime import datetime


def get_weather(lon, lat, city, date, source):
    history_obj = db.get_or_create_weather_history(city, lon, lat, date)
    db_res = db.get_weather_detail(history_obj['stat_id'], source)

    if db_res:
        return _fetch_result_text(db_res, history_obj, source)

    yandex.fill_yandex_weather(history_obj)
    gismeteo.fill_gismeteo_weather(history_obj)

    db_res = db.get_weather_detail(history_obj['stat_id'], source)
    return _fetch_result_text(db_res, history_obj, source)


def _fetch_result_text(wheather_details, history_obj, source):
    result = 'Погода в городе: %s на %s по прогозу %s\n\nНочью: %s\nУтром:%s\nДнём: %s\nВечером: %s'

    for instance in wheather_details:
        if instance['part'] == 'morning':
            morning = _set_sub_stroke(instance)
        if instance['part'] == 'day':
            day = _set_sub_stroke(instance)
        if instance['part'] == 'night':
            night = _set_sub_stroke(instance)
        if instance['part'] == 'evening':
            evening = _set_sub_stroke(instance)
    date = datetime.strptime(history_obj['dt'], '%Y-%m-%d').strftime('%d.%m.%Y')
    source_stroke = _get_source_rus(source)
    return result % (history_obj['city'], date, source_stroke, night, morning, day, evening)


def _get_source_rus(source):
    if source == 'yandex':
        return 'Яндекс'
    if source == 'gismeteo':
        return 'Гисметео'


def _set_sub_stroke(obj):
    sub_stroke = '\nТемпература: %s°C.\nОсадки: %s.\nНаправление ветра: %s\nСкорость ветра: %s м/с\
        \nДавление: %s мм\nВлажность: %s \n'
    result = sub_stroke % (obj['temp_avg'], obj['prec_type'], obj['wind_dir'].title(),
                           obj['wind_speed'], obj['pressure_mm'], str(obj['humidity']) + '%')
    return result
