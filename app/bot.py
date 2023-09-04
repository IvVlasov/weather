from data import db
from settings import bot
from services import geocoder, weather
from telebot import types
from datetime import datetime, timedelta


def main_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Получить прогноз", request_location=True))
    keyboard.add(types.KeyboardButton(text="Изменить город", request_location=True))
    return keyboard


def request_loc_btns():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    return keyboard


def request_day_message(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="Сегодня", callback_data='day_today'))
    keyboard.add(types.InlineKeyboardButton(text="Завтра", callback_data='day_tomorrow'))
    answer = 'Выберите день'
    bot.send_message(message.chat.id, answer, reply_markup=keyboard)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    db.create_user(message.chat.id)
    answer = 'Я магический бот, который предсказывает БУДУЩЕЕ...\nну погоду.\n\nОтправь своё местоположение '\
             'чтобы получить магический прогноз. Можешь также ввести название города.'
    bot.send_message(message.chat.id, answer, reply_markup=request_loc_btns())


@bot.message_handler(func=lambda msg: msg.text != 'Получить прогноз' and msg.text != 'Настройки')
def get_city(message):
    city_text = message.text
    result = geocoder.get_coorditates_by_city(city_text)
    if not result:
        answer = 'Мы не смогли найти ваш город 😔\nПопробуйте ещё раз.'
        bot.send_message(message.chat.id, answer, reply_markup=request_loc_btns())
        return
    lon, lat, city = result
    db.set_user_coords(message.chat.id, lon, lat, city)
    request_day_message(message)


@bot.message_handler(content_types=['location'])
def location(message):
    lon, lat = message.location.longitude, message.location.latitude
    city = geocoder.get_city_by_coordinates(lon, lat)
    if not city:
        answer = 'Мы не смогли найти ваш город 😔\nПопробуйте ещё раз.'
        bot.send_message(message.chat.id, answer, reply_markup=request_loc_btns())
        return
    db.set_user_coords(message.chat.id, lon, lat, city)
    request_day_message(message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('day'))
def choose_day(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    day = call.data.split('_')[1]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="Яндекс", callback_data='source_'+day+'_yandex'))
    keyboard.add(types.InlineKeyboardButton(text="Гисметео", callback_data='source_'+day+'_gismeteo'))

    answer = 'Выберите источник'
    bot.send_message(call.message.chat.id, answer, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('source'))
def choose_source(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    call_data = call.data.split('_')
    day = call_data[1]
    source = call_data[2]

    dt = datetime.today()
    if day == 'tomorrow':
        dt = dt + timedelta(days=1)

    lon, lat, city = db.get_user_coords(call.message.chat.id)
    answer = weather.get_weather(lon, lat, city, dt, source)

    if source == 'yandex':
        another = 'gismeteo'
        another_text = 'Прогноз Гисметео'
    if source == 'gismeteo':
        another = 'yandex'
        another_text = 'Прогноз Яндекса'

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text=another_text, callback_data='source_'+day+'_'+another))
    bot.send_message(call.message.chat.id, answer, reply_markup=keyboard)


if __name__ == '__main__':
    bot.infinity_polling()
