import telebot
import os

DB_PATH = 'database.db'
BOT_TOKEN = os.getenv('BOT_API_TOKEN')
GEO_TOKEN = os.getenv('GEO_API_TOKEN')
WEATHER_TOKEN = os.getenv('WEATHER_API_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)
