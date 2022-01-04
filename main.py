import telebot
from aiogram.types import KeyboardButtonPollType, ReplyKeyboardMarkup, ReplyKeyboardRemove, Poll, CallbackQuery
from telebot import types
from telebot.types import KeyboardButton
from telegram import Message

from Facts import Facts
from Games import *
from Lectures import *
from Recomendations import *
from Test import *
from transliterate.decorators import transliterate_function

bot = telebot.TeleBot('token')


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
        keyboard.add(types.InlineKeyboardButton(text='Дієслово (Verb)', callback_data='1'))
        keyboard.add(types.InlineKeyboardButton(text='Герундій (Gerund)', callback_data='2'))
        keyboard.add(types.InlineKeyboardButton(text='Інфінітив (Infinitive)', callback_data='3'))
        keyboard.add(types.InlineKeyboardButton(text='Неправильні дієслова (Irregular Verbs)', callback_data='4'))
        keyboard.add(types.InlineKeyboardButton(text='Фразові дієслова (Phrasal Verbs)', callback_data='5'))
        keyboard.add(*[types.InlineKeyboardButton(name, callback_data=name) for name in ['◀', '▶']])
        bot.send_message(message.from_user.id, "Оберіть з наступних лекцій:", reply_markup=keyboard)
    elif message.text == "Що подивитись/почитати?":
        url_button = types.InlineKeyboardButton(text="Тест на рівень англійської",
                                                url="https://talkstudio.com.ua/placement-test/")
        key_level = types.InlineKeyboardButton(text='Я знаю свій рівень:', callback_data='answer')
        keyboard.add(url_button)
        keyboard.add(key_level)
        bot.send_message(message.from_user.id, "Ти знаєш свій рівень англійської?", reply_markup=keyboard)
    elif message.text == "Тести":
        key_test = types.InlineKeyboardButton(text='Розпочати', callback_data='tests')
        keyboard.add(key_test)
        bot.send_message(message.from_user.id, "Дай 5 правильних відповідей і отримай бонус", reply_markup=keyboard)
    else:
        bot.reply_to(message, "Не можу зрозуміти Ваше повідомлення.\n Введіть /help.")


level = ""
a = 5
test = Test()
score = 0
isLection = False
count = 0


@bot.message_handler(content_types=['text'])
def handle_text(message):
    global level
    level = translit(message.text)
    levels = ["A1", "A2", "B1", "B2", "C1"]
    if level in levels:
        bot.send_message(message.chat.id, "Ваш рівень: " + level)
        keyboard = types.InlineKeyboardMarkup()
        key_film = types.InlineKeyboardButton(text='Фільм', callback_data='film')
        keyboard.add(key_film)
        key_book = types.InlineKeyboardButton(text='Книга', callback_data='book')
        keyboard.add(key_book)
        bot.send_message(message.from_user.id, "Що ви хочете отримати?:", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Невірно введений рівень")
        bot.register_next_step_handler(message, handle_text)
        bot.send_message(message.chat.id, "Введіть ваш рівень англійської: ")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    keyboard = types.InlineKeyboardMarkup()
    global a, test, isLection
    dict_game = {"words": FirstLetterGame(), "cipher": MixGame(), "translate": TranslatorGame(),
                 "riddles": PuzzleGame()}
    list_recommend = ["film", "book"]
    if call.data == "answer":
        bot.register_next_step_handler(call.message, handle_text)
        bot.send_message(call.message.chat.id, "Введіть ваш рівень англійської: ")
    elif call.data == "tests":
        if isLection:
            test = Test(test.topic)
        else:
            test = Test()
        bot.send_message(call.message.chat.id, test)
        bot.send_message(call.message.chat.id, "Введіть відповідь: ")
        bot.register_next_step_handler(call.message, test_handler)
    elif call.data in dict_game:
        bot.send_message(call.message.chat.id, dict_game[call.data])
    elif call.data in data.keys():
        lecture = Lectures(call.data)
        if len(str(lecture)) > 4096:
            for x in range(0, len(str(lecture)), 4096):
                bot.send_message(call.message.chat.id, str(lecture)[x:x + 4096])
        else:
            bot.send_message(call.message.chat.id, lecture)
        bot.send_photo(call.message.chat.id, lecture.image)
        test = Test(lecture.index)
        isLection = True
        keyboard.add(types.InlineKeyboardButton(text='Розпочати', callback_data='tests'))
        bot.send_message(call.message.chat.id, "Для засвоєння матеріалу пройдіть короткий тест за темою лекції", reply_markup=keyboard)
    elif call.data == "◀":
        a -= 10
        if a < 0:
            return
        for i in range(5):
            a += 1
            lecture = Lectures(str(a))
            keyboard.add(types.InlineKeyboardButton(text=lecture.name, callback_data=lecture.index))
        keyboard.add(*[types.InlineKeyboardButton(name, callback_data=name) for name in ['◀', '▶']])
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    elif call.data == "▶":
        if a > 10:
            return
        for i in range(5):
            a += 1
            lecture = Lectures(str(a))
            keyboard.add(types.InlineKeyboardButton(text=lecture.name, callback_data=lecture.index))
        keyboard.add(*[types.InlineKeyboardButton(name, callback_data=name) for name in ['◀', '▶']])
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    elif call.data in list_recommend:
        recommend = get_recommend(call.data, level)
        bot.send_photo(call.message.chat.id, recommend.image(), caption=recommend.description())


@transliterate_function(language_code='ru', reversed=True)
def translit(text):
    return text.upper()


@bot.message_handler(content_types=['text'])
def test_handler(message):
    global score, test, count, isLection
    answer_quest = message.text
    if answer_quest in ['Тести', "Лекції", "Ігри", "Що подивитись/почитати?"]:
        score = 0
        count = 0
        incorrect_cmd(message)
        return
    bot.send_message(message.chat.id, test.passing_test(answer_quest))
    score += test.score
    count += 1
    if count == 5:
        bot.send_message(message.chat.id, f"Your score: {score}")
        if score == 5:
            fact = Facts()
            bot.send_message(message.chat.id, f"Fun fact: {fact}")
        score = 0
        count = 0
        isLection = False
        return
    callback_worker(CallbackQuery(data='tests', message=message))


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)

