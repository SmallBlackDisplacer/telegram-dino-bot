import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)


# хранилище состояния пользователей
user_data = {}

# вопросы
questions = [
    {
        "text": "Подробно опиши, какой ты человек, что формирует тебя как личность?",
        "options": ["Я пидор", "Ты пидор", "Хуй жопа говно"]
    },
    {
        "text": "Любишь динозавров?",
        "options": ["Да", "Очень", "Предпочитаю дрочить"]
    },
    {
        "text": "Что ты любишь есть?",
        "options": ["Говно", "Хуй", "Христианских младенцев"]
    },
    {
        "text": "Место, где ты можешь быть собой",
        "options": ["Ад", "Израиль", "Гейская оргия"]
    }
]


# старт
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_data[user_id] = {
        "step": "name",
        "answers": []
    }
    bot.send_message(user_id, "Узнай, какой ты динозавр! 🦖\nКак тебя зовут?")


# обработка всех сообщений
@bot.message_handler(func=lambda message: True)
def handle(message):
    user_id = message.chat.id

    if user_id not in user_data:
        bot.send_message(user_id, "Узнай, какой ты динозавр! 🦖\nНапиши /start чтобы начать")
        return

    state = user_data[user_id]

    # 1. ввод имени
    if state["step"] == "name":
        state["name"] = message.text
        state["step"] = 0

        send_question(user_id)
        return

    # 2. ответы на вопросы
    step = state["step"]

    if step < len(questions):
        state["answers"].append(message.text)
        state["step"] += 1

        if state["step"] < len(questions):
            send_question(user_id)
        else:
            send_result(user_id)


def send_question(user_id):
    step = user_data[user_id]["step"]
    q = questions[step]

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    for option in q["options"]:
        markup.add(option)

    bot.send_message(user_id, q["text"], reply_markup=markup)


def send_result(user_id):
    name = user_data[user_id]["name"]
    answers = user_data[user_id]["answers"]

    # простая логика результата
    if name == 'Денис' or "Израиль" in answers or "Христианских младенцев" in answers:
        result = "Ты жидорептилоид ✡️ 🦖 ✡️"
        result_img = "jdino.jpg"
    else:
        result = "Ты долбоящер 🦕"
        result_img = "dino.jpg"

    bot.send_message(
        user_id,
        f"{name}, вот какой ты динозавр:\n\n{result}",
        reply_markup=telebot.types.ReplyKeyboardRemove()
    )
    with open(result_img, "rb") as photo:
        bot.send_photo(user_id, photo)

    # очистка данных
    del user_data[user_id]


bot.infinity_polling()
