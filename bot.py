from telebot import *
import random


class Words:
    def init(self):
        pass

    def str(self):
        return f'ApplE'


class Cipher:
    def init(self):
        pass

    def str(self):
        return f'paple'


class Translate:
    def init(self):
        pass

    def str(self):
        return f'яблуко'


class Riddle:
    def init(self):
        pass

    def str(self):
        return f'New York is also called: "Big ...'


class Game:
    def init(self):
        self.keyboard = types.InlineKeyboardMarkup()
        self.key_word = types.InlineKeyboardButton(text='Слова', callback_data='words')
        self.key_cipher = types.InlineKeyboardButton(text='Шифр', callback_data='cipher')
        self.key_translate = types.InlineKeyboardButton(text='Перекладач', callback_data='translate')
        self.key_riddles = types.InlineKeyboardButton(text='Загадки', callback_data='riddles')

    def games_keyboard(self):
        self.keyboard.add(self.key_word)
        self.keyboard.add(self.key_cipher)
        self.keyboard.add(self.key_translate)
        self.keyboard.add(self.key_riddles)

    def str(self):
        return f'Games'


class Lections:
    def init(self):
        pass

    def str(self):
        return f'List of lections'


class Test:
    def init(self):
        pass

    def str(self):
        return f'Random test'


class Film():
    def init(self):
        self.film = "Titanic"

    def str(self):
        return f'I recommend you to watch {self.film}'


class Book():
    def init(self):
        self.book = "Harry Potter"

    def str(self):
        return f'I recommend you to read {self.book}'


class Recomend:
    def init(self):
        self.book = Book()
        self.film = Film()
        self.listch = []
        self.listch.append(self.book)
        self.listch.append(self.film)
        self.keyboard2 = types.InlineKeyboardMarkup()
        self.url_button = types.InlineKeyboardButton(text="Тест на рівень англійської",
                                                     url="https://talkstudio.com.ua/placement-test/")
        self.key_level = types.InlineKeyboardButton(text='Я знаю свій рівень:', callback_data='answer')

    def recomend_keyboard(self):
        self.keyboard2.add(self.url_button)
        self.keyboard2.add(self.key_level)

    def str(self):
        return f'{random.choice(self.listch)}'


bot = telebot.TeleBot("Token")


@bot.message_handler(commands="start")
def cmd_start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Tests', 'Lections']])
    keyboard.add(*[types.KeyboardButton(name) for name in ['Games', 'Recomendation']])
    bot.send_message(message.from_user.id, "Choose what you want:", reply_markup=keyboard)


@bot.message_handler(commands="help")
def cmd_help(message):
    bot.reply_to(message, "It is bot for learning English. In order to begin write /start")


@bot.message_handler(func=lambda mes: True)
def incorrect_cmd(message):
    dict_choise = {"Recomendation": Recomend(), "Tests": Test(), "Lections": Lections(), "Games": Game()}
    if message.text in dict_choise.keys():
        if message.text == "Games":
            ob = Game()
            ob.games_keyboard()
            bot.send_message(message.from_user.id, "Обери гру:", reply_markup=ob.keyboard)
        if message.text == "Recomendation":
            ob = Recomend()
            ob.recomend_keyboard()
            bot.send_message(message.from_user.id, "Ти знаєш свій рівень англійської?", reply_markup=ob.keyboard2)
        else:
            bot.send_message(message.from_user.id, dict_choise[message.text])
    else:
        bot.reply_to(message, "I don’t understand you.\n Write /help.")

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    dict_game = {"words": Words(), "cipher": Cipher(), "translate": Translate(), "riddles": Riddle()}
    if call.data == "answer":
        bot.send_message(call.from_user.id, "You level:B1")
        bot.send_message(call.from_user.id, Recomend())
    if call.data in dict_game:
        bot.send_message(call.from_user.id, dict_game[call.data])
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


bot.polling(none_stop=True, interval=0)