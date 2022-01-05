import asyncio

from Recomendations import *
from Games import *
from Lectures import *
from Test import *
import telebot
from telebot import types

bot = telebot.TeleBot('token')
bot.__setattr__('windows', dict)


@bot.message_handler(commands="start")
def cmd_start(message):
    bot.reply_to(message, "Привіт, " + message.from_user.first_name + "! Я - бот для вивчення англійської.")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Тести', 'Лекції']])
    keyboard.add(*[types.KeyboardButton(name) for name in ['Ігри', 'Що подивитись/почитати?']])
    bot.send_message(message.from_user.id, "Оберіть з наступних опцій:", reply_markup=keyboard)


@bot.message_handler(commands="help")
def cmd_help(message):
    bot.reply_to(message, "Введіть /start для початку роботи.")


@bot.message_handler(func=lambda mes: True)
def incorrect_cmd(message):
    keyboard = types.InlineKeyboardMarkup()
    if message.text == "Ігри":
        key_word = types.InlineKeyboardButton(text='Слова', callback_data='words')
        key_cipher = types.InlineKeyboardButton(text='Розшифруй слово', callback_data='cipher')
        key_translate = types.InlineKeyboardButton(text='Перекладач', callback_data='translate')
        key_riddles = types.InlineKeyboardButton(text='Загадки', callback_data='riddles')
        keyboard.add(key_word)
        keyboard.add(key_cipher)
        keyboard.add(key_translate)
        keyboard.add(key_riddles)
        bot.send_message(message.from_user.id, "Обери гру:", reply_markup=keyboard)
    elif message.text == "Лекції":
        key_lecture1 = types.InlineKeyboardButton(text='1. Англійський іменник', callback_data='lecture1')
        keyboard.add(key_lecture1)
        key_lecture2 = types.InlineKeyboardButton(text='2. Англійський прикметник', callback_data='lecture2')
        keyboard.add(key_lecture2)
        bot.send_message(message.from_user.id, "Оберіть з наступних лекцій:", reply_markup=keyboard)
    elif message.text == "Що подивитись/почитати?":
        url_button = types.InlineKeyboardButton(text="Тест на рівень англійської",
                                                url="https://talkstudio.com.ua/placement-test/")
        key_level = types.InlineKeyboardButton(text='Я знаю свій рівень:', callback_data='answer')
        keyboard.add(url_button)
        keyboard.add(key_level)
        bot.send_message(message.from_user.id, "Ти знаєш свій рівень англійської?", reply_markup=keyboard)
    elif message.text == "Тести":
        bot.send_message(message.from_user.id, Test())
    else:
        bot.reply_to(message, "Не можу зрозуміти Ваше повідомлення.\n Введіть /help.")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if issubclass(bot.__getattribute__('windows')[message.chat.id], Game):
        if message.text == bot.__getattribute__('windows')[message.chat.id].right_answer:
            bot.__getattribute__('windows')[message.chat.id].exit(True)
        else:
            bot.send_message(message.chat.id, 'Не правильно')
    else:
        level = message.text
        levels = ["A1", "A2", "B1", "B2", "C1"]
        if level in levels:
            bot.send_message(message.chat.id, "Ваш рівень: " + level)
            bot.send_message(message.chat.id, Recomendations(level))
        else:
            bot.send_message(message.chat.id, "Невірно введений рівень")
            bot.register_next_step_handler(message, handle_text)
            bot.send_message(message.chat.id, "Введіть ваш рівень англійської: ")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    dict_game = {"words": FirstLetterGame(), "cipher": MixGame(), "translate": TranslatorGame(),
                 "riddles": PuzzleGame()}
    window = bot.__getattribute__('windows')[call.from_user.id]
    # if issubclass(window, Game):
    if call.data == 'start':
        window.start()
        while window.is_started:
            bot.register_next_step_handler(call.message, handle_text)
    elif call.data == 'rules':
        bot.send_message(call.from_user.id, window.rules)
    elif call.data == 'difficulty':
        call.from_user.id, window.change_difficulty()
    elif call.data == 'back':
        window = None
        incorrect_cmd(message=bot.send_message(call.from_user.id, 'Ігри'))
    # else:
    # dict_game = {"words": FirstLetterGame(), "cipher": MixGame(), "translate": TranslatorGame(),
    #              "riddles": PuzzleGame()}
    elif call.data == "answer":
        bot.register_next_step_handler(call.message, handle_text)
        bot.send_message(call.message.chat.id, "Введіть ваш рівень англійської: ")
    elif call.data in dict_game:
        bot.__getattribute__('windows')[call.from_user.id] = dict_game[call.data]()
        bot.send_message(call.from_user.id, 'меню гри: ' + call.data, reply_markup= \
            bot.__getattribute__('windows')[call.from_user.id].get_keyboard())
    elif call.data in data.keys():
        lecture = Lectures(call.data)
        bot.send_message(call.message.chat.id, lecture)


bot.polling(none_stop=True, interval=0)
