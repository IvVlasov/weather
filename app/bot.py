from settings import bot
from services import db, geocoder, yandex
from telebot import types
from datetime import datetime, timedelta


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    db.create_user(message.chat.id)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    answer = 'Я магический бот, который предсказывает БУДУЩЕЕ...\nну погоду.\n\nОтправь своё местоположение '\
    'чтобы получить магический прогноз. Можешь также ввести название города.'
    bot.send_message(message.chat.id, answer, reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def location(message):
    if message.location is not None:
        lon, lat = message.location.longitude, message.location.latitude
        city = geocoder.get_city_by_coordinates(lon, lat)
        db.set_user_coords(message.chat.id, lon, lat, city)

        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Сегодня"), types.KeyboardButton(text="Завтра"))

        answer = 'Выберите день'
        bot.send_message(message.chat.id, answer, reply_markup=keyboard)


@bot.message_handler()
def send_weather(message):
    if message.text == 'Сегодня':
        date_now = datetime.today()
    elif message.text == 'Завтра':
        date_now = datetime.today() + timedelta(days=1)

    lon, lat = db.get_user_coords(message.chat.id)
    yandex.get_weather(lon, lat, date_now)

    print('asbdjl')
    pass


if __name__ == '__main__':
    bot.infinity_polling()
