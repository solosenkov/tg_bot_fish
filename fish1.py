import os
import pip
from flask import Flask, request
import telebot
from faker import Faker
from background import keep_alive


bot = telebot.TeleBot("YOUR_TOKEN")

# фейкер (язык русский) - если в скобках ничего не указано - то язык английский
fake = Faker('ru_RU')


app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "ok", 200
    else:
        return "Hello, I'm a bot!", 200


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Ку-ку! Я бот для генерации рыбного текста. Введи любое число (от 1 до 1499) и я сгенерирую текст.")


@bot.message_handler(func=lambda message: True)
def generate_text(message):
    try:
        length = int(message.text.strip())
        if 1 <= length <= 1499:
            text = fake.text(length)
            bot.send_message(message.chat.id, text)
        else:
            bot.send_message(message.chat.id, "Неверное количество символов. Введите !ЧИСЛО! от 1 до 1499.")
    except ValueError:
        bot.send_message(message.chat.id, "Введите число от 1 до 1499.")


if __name__ == '__main__':
    keep_alive()
    bot.polling(none_stop=True)
