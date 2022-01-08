# from aiogram.types import CallbackQuery
from Classes.Facts import Facts
from Classes.Games import FirstLetterGame, PuzzleGame, TranslatorGame, MixGame, Game
from Classes.Lectures import *
from Classes.Recomendations import *
from Classes.Test import *
from transliterate.decorators import transliterate_function
from Classes.BotWithUsers import BotWithPages
import keyboards
# from telebot import types
from Data import token

# from typing import Callable

bot = BotWithPages(token)


@bot.message_handler(commands="start")
def cmd_start(message):
    bot.reply_to(message, "Привіт, " + message.from_user.first_name + "! Я - бот для вивчення англійської.")
    bot.send_message(message.from_user.id, "Оберіть з наступних опцій:", reply_markup=[keyboards.MainKeyboard.keyboard])
    bot.set_user(message.from_user.id)


@bot.message_handler(commands="help")
def cmd_help(message):
    bot.reply_to(message, "Введіть /start для початку роботи.")


@bot.message_handler(func=lambda mes: True)
def incorrect_cmd(message):
    if message.text == "Ігри":
        bot.send_message(message.from_user.id, "Обери гру:", reply_markup=[Game.get_keyboard()])
    elif message.text == "Лекції":
        bot.send_message(message.from_user.id, "Оберіть з наступних лекцій:",
                         reply_markup=[Lectures.get_keyboard(bot.get_user(message.chat.id).number)])
    elif message.text == "Що подивитись/почитати?":
        bot.send_message(message.from_user.id, "Ти знаєш свій рівень англійської?",
                         reply_markup=[keyboards.LevelKeyboard.keyboard])
    elif message.text == "Тести":
        bot.send_message(message.from_user.id, "Дай 5 правильних відповідей і отримай бонус",
                         reply_markup=[keyboards.TestKeyboard.keyboard])
    else:
        if issubclass(type(bot.get_user(message.chat.id).page), Game):
            if message.text == bot.get_user(message.chat.id).page.right_answer:
                bot.get_user(message.chat.id).page.stop(True)
                # bot.send_message(message.chat.id, 'меню гри', reply_markup= \
                #     bot.get_user(message.chat.id).page.keyboard)
            else:
                bot.send_message(message.chat.id, 'Не правильно')
        elif issubclass(type(bot.get_user(message.chat.id).page), Lectures):
            level = translit(message.text)
            levels = ["A1", "A2", "B1", "B2", "C1"]
            if level in levels:
                bot.send_message(message.chat.id, "Ваш рівень: " + level)
                bot.send_message(message.from_user.id, "Що ви хочете отримати?:",
                                 reply_markup=keyboards.RecommendKeyboard.keyboard)
            else:
                bot.send_message(message.chat.id, "Невірно введений рівень")
                bot.send_message(message.chat.id, "Введіть ваш рівень англійської: ")
        elif issubclass(type(bot.get_user(message.chat.id).page), Test):
            global test
            answer_quest = message.text
            bot.send_message(message.chat.id, test.passing_test(answer_quest))
            bot.get_user(message.chat.id).score += test.score
            score = bot.get_user(message.chat.id).score
            if True:
                used_tests.clear()
                bot.send_message(message.chat.id, f"Your score: {score}")
                if score == 5:
                    fact = Facts()
                    bot.send_message(message.chat.id, f"Fun fact: {fact}")
                bot.get_user(message.chat.id).score = 0
                # bot.get_user(message.chat.id).close_page()
                return
            # callback_worker(CallbackQuery(data='tests', message=message))
        else:
            bot.reply_to(message, "Не можу зрозуміти Ваше повідомлення.\n Введіть /help.")


test = Test()


used_tests = []


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global used_tests
    # keyboard = types.InlineKeyboardMarkup()
    global test
    dict_game = {"words": FirstLetterGame, "cipher": MixGame, "translate": TranslatorGame,
                 "riddles": PuzzleGame}
    list_recommend = ["film", "book"]
    if bot.get_user(call.from_user.id).page:
        if issubclass(type(bot.get_user(call.from_user.id).page), Game):
            if call.data == 'start':
                bot.get_user(call.from_user.id).page.start()
            elif call.data == 'rules':
                bot.send_message(call.from_user.id, str(bot.get_user(call.from_user.id)))
            elif call.data == 'difficulty':
                bot.get_user(call.from_user.id).page.change_difficulty()
            elif call.data == 'back':
                # bot.get_user(call.from_user.id).close_page()
                bot.get_user(call.from_user.id).page = None
                bot.send_message(call.from_user.id, 'Обери гру: ', reply_markup=[Game.get_keyboard()])
        elif issubclass(type(bot.get_user(call.from_user.id).page), Lectures):
            if call.data == 'back':
                bot.get_user(call.from_user.id).page = None
                bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=[
                    Lectures.get_keyboard(bot.get_user(call.from_user.id).number)])
            elif False:
                test = Test(test.topic)
                while test.questions in used_tests:
                    if isinstance(bot.get_user(call.from_user.id).page, Lectures):
                        test = Test(test.topic)
                    else:
                        test = Test()
                used_tests.append(test.questions)
                bot.send_message(call.from_user.id, str(test))
                bot.send_message(call.from_user.id, "Введіть відповідь: ")
    elif call.data == "answer":
        bot.send_message(call.from_user.id, "Введіть ваш рівень англійської: ")
    elif call.data == "tests":
        test = Test()
        while test.questions in used_tests:
            if isinstance(bot.get_user(call.from_user.id).page, Lectures):
                test = Test(test.topic)
            else:
                test = Test()
        used_tests.append(test.questions)
        bot.send_message(call.from_user.id, str(test))
        bot.send_message(call.from_user.id, "Введіть відповідь: ")
    elif call.data in dict_game:
        bot.get_user(call.from_user.id).page = dict_game[call.data](bot, call.from_user.id)
    elif call.data in data.keys():
        lecture = Lectures(call.data)
        bot.get_user(call.from_user.id).page = lecture
        if len(str(lecture)) > 4096:
            for x in range(0, len(str(lecture)), 4096):
                bot.send_message(call.from_user.id, str(lecture)[x:x + 4096])
        else:
            bot.send_message(call.from_user.id, str(lecture))
        bot.send_photo(call.from_user.id, lecture.image)
        test = Test(lecture.index)
        bot.send_message(call.from_user.id, "Для засвоєння матеріалу пройдіть короткий тест за темою лекції",
                         reply_markup=[lecture.keyboard])
    elif call.data == "◀":
        bot.get_user(call.from_user.id).number -= 1
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, \
                                      reply_markup=[Lectures.get_keyboard(bot.get_user(call.from_user.id).number)])
    elif call.data == "▶":
        bot.get_user(call.from_user.id).number += 1
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, \
                                      reply_markup=[Lectures.get_keyboard(bot.get_user(call.from_user.id).number)])
    elif call.data in list_recommend:
        recommend = get_recommend(call.data, bot.get_user(call.from_user.id).level)
        bot.send_photo(call.from_user.id, recommend.image(), caption=recommend.description())


@transliterate_function(language_code='ru', reversed=True)
def translit(text):
    return text.upper()


# @bot.message_handler(content_types='text')
# def test_handler(message):


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
