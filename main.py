import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id, "Узнай, какой ты динозавр! 🦖\nКак тебя зовут?")


@bot.message_handler(func=lambda message: True)
def get_name(message):
    name = message.text.strip().lower()

    if name == "вася":
        bot.send_message(message.chat.id, "Ты долбоящер! 🦖")
        with open("dino.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, "Ты долбоящер! 🦕")
        with open("dino.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo)


bot.infinity_polling()