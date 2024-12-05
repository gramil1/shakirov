import telebot, requests, os
from datetime import datetime
from dotenv import load_dotenv 

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))

#API_KEY_TELEGRAM = '6235787065:AAFnJEsKJhIT0eyT74ZIF9HZPUB3yGqvCuQ'
API_KEY_WEATHER = '76dc0b46b198b8ae0232f4fd5d7b4903'

#bot = telebot.TeleBot(API_KEY_TELEGRAM)

def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': API_KEY_WEATHER,
        'lang': 'ru',
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if response.status_code == 200:
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        return f"Погода в {city}: {weather}, температура: {temp}°C"
    else:
        return "Не удалось получить данные о погоде. Проверьте название города."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Напиши название города, и я расскажу тебе погоду.")

@bot.message_handler(func=lambda message: True)
def send_weather(message):
    city = message.text
    weather_info = get_weather(city)
    bot.reply_to(message, weather_info)

bot.polling()