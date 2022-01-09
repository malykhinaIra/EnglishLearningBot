from Classes.Facts import Facts
from Classes.Level import Level
from Classes.Games import FirstLetterGame, PuzzleGame, TranslatorGame, MixGame, Game
from Classes.Lectures import Lectures, data
from Classes.Recomendations import get_recommend
from Classes.Test import Test
from transliterate.decorators import transliterate_function
from Classes.BotWithUsers import BotWithPages
from Data import token
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bot = BotWithPages(token)


@bot.message_handler(commands="start")
def cmd_start(message):
    bot.reply_to(message, "Привіт, " + message.from_user.first_name + "! Я - бот для вивчення англійської.")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*[KeyboardButton(name) for name in ['Тести', 'Лекції']])
    keyboard.add(*[KeyboardButton(name) for name in ['Ігри', 'Що подивитись/почитати?']])
    bot.send_message(message.from_user.id, "Оберіть з наступних опцій:", reply_markup=[keyboard])
    bot.set_user(message.from_user.id)


@bot.message_handler(commands="help")
def cmd_help(message):
    bot.reply_to(message, "Введіть /start для початку роботи.")


@bot.message_handler(func=lambda mes: True)
def incorrect_cmd(message):
    if bot.get_user(message.from_user.id):
        if message.text == "Ігри":
            bot.get_user(message.from_user.id).page = None
            bot.send_message(message.from_user.id, "Обери гру:", reply_markup=[Game.get_keyboard()])
        elif message.text == "Лекції":
            bot.get_user(message.from_user.id).page = None
            bot.send_message(message.from_user.id, "Оберіть з наступних лекцій:",
                             reply_markup=[Lectures.get_keyboard(bot.get_user(message.chat.id).number)])
        elif message.text == "Що подивитись/почитати?":
            bot.get_user(message.from_user.id).page = bot.get_user(message.from_user.id).level
            bot.send_message(message.from_user.id, "Ти знаєш свій рівень англійської?" if
                             bot.get_user(message.from_user.id).page.level == "None" else "Меню",
                             reply_markup=[bot.get_user(message.from_user.id).level.keyboard])
        elif message.text == "Тести":
            bot.get_user(message.from_user.id).page = None
            bot.send_message(message.from_user.id, "Дай 5 правильних відповідей і отримай бонус",
                             reply_markup=[Test.get_keyboard()])
        else:
            if issubclass(type(bot.get_user(message.chat.id).page), Game):
                if bot.get_user(message.chat.id).page.set_answer(message.text):
                    bot.get_user(message.chat.id).page.stop(True)
                else:
                    bot.send_message(message.chat.id, 'Не правильно')
            elif issubclass(type(bot.get_user(message.chat.id).page), Level):
                level = translate(message.text)
                try:
                    bot.get_user(message.chat.id).level = level
                    bot.send_message(message.chat.id, "Ваш рівень: " + level)
                    bot.send_message(message.from_user.id, "Що ви хочете отримати?:",
                                     reply_markup=[bot.get_user(message.chat.id).level.keyboard])
                except...:
                    bot.send_message(message.chat.id, "Невірно введений рівень")
                    bot.send_message(message.chat.id, "Введіть ваш рівень англійської: ")
            elif issubclass(type(bot.get_user(message.chat.id).page), Test):
                answer_quest = message.text
                bot.send_message(message.chat.id, bot.get_user(message.chat.id).page.passing_test(answer_quest))
                bot.get_user(message.chat.id).page.next_task()
                if bot.get_user(message.chat.id).page.sentence:
                    bot.send_message(message.chat.id, str(bot.get_user(message.chat.id).page))
                    bot.send_message(message.chat.id, "Введіть відповідь: ")
                else:
                    bot.get_user(message.chat.id).add_score(bot.get_user(message.chat.id).page.score)
                    bot.send_message(message.chat.id, 'Тест завершено')
                    bot.send_message(message.chat.id, f"Ваш рахунок: {bot.get_user(message.chat.id).page.score}")
                    if bot.get_user(message.chat.id).page.score == 15:
                        fact = Facts()
                        bot.send_message(message.chat.id, f"Fun fact: {fact}")
                    bot.get_user(message.chat.id).page = None
            else:
                bot.reply_to(message, "Не можу зрозуміти Ваше повідомлення.\n Введіть /help.")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    dict_game = {"words": FirstLetterGame, "cipher": MixGame, "translate": TranslatorGame,
                 "riddles": PuzzleGame}
    if bot.get_user(call.from_user.id).page:
        if issubclass(type(bot.get_user(call.from_user.id).page), Game):
            if call.data == 'start':
                bot.get_user(call.from_user.id).page.start()
            elif call.data == 'rules':
                bot.send_message(call.from_user.id, str(bot.get_user(call.from_user.id).page))
            elif call.data == 'difficulty':
                bot.get_user(call.from_user.id).page.change_difficulty()
            elif call.data == 'back':
                bot.get_user(call.from_user.id).page = None
                bot.send_message(call.from_user.id, 'Обери гру: ', reply_markup=[Game.get_keyboard()])
        elif issubclass(type(bot.get_user(call.from_user.id).page), Lectures):
            if call.data == 'back':
                bot.get_user(call.from_user.id).page = None
                bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=[
                    Lectures.get_keyboard(bot.get_user(call.from_user.id).number)])
            elif call.data == 'test':
                bot.get_user(call.from_user.id).page = Test(bot.get_user(call.from_user.id).page.index)
                bot.send_message(call.from_user.id, str(bot.get_user(call.from_user.id).page))
                bot.send_message(call.from_user.id, "Введіть відповідь: ")
        elif issubclass(type(bot.get_user(call.from_user.id).page), Level):
            if call.data == 'up':
                bot.get_user(call.from_user.id).level.up_level()
                bot.send_message(call.from_user.id, "Ваш рівень: " + bot.get_user(call.from_user.id).level.level)
            elif call.data == 'down':
                bot.get_user(call.from_user.id).level.down_level()
                bot.send_message(call.from_user.id, "Ваш рівень: " + bot.get_user(call.from_user.id).level.level)
            elif call.data == "answer":
                bot.send_message(call.from_user.id, "Введіть ваш рівень англійської: ")
            elif call.data == 'book' or call.data == 'film':
                recommend = get_recommend(call.data, bot.get_user(call.from_user.id).level.level)
                bot.send_photo(call.from_user.id, recommend.image(), caption=recommend.description())
    elif call.data == "tests":
        bot.get_user(call.from_user.id).page = Test()
        bot.send_message(call.from_user.id, str(bot.get_user(call.from_user.id).page))
        bot.send_message(call.from_user.id, "Введіть відповідь: ")
    elif call.data in dict_game:
        bot.get_user(call.from_user.id).page = dict_game[call.data](bot, call.from_user.id)
    elif call.data in data.keys():
        bot.get_user(call.from_user.id).page = Lectures(call.data)
        if len(str(bot.get_user(call.from_user.id).page)) > 4096:
            for x in range(0, len(str(bot.get_user(call.from_user.id).page)), 4096):
                bot.send_message(call.from_user.id, str(bot.get_user(call.from_user.id).page)[x:x + 4096])
        else:
            bot.send_message(call.from_user.id, str(bot.get_user(call.from_user.id).page))
        bot.send_photo(call.from_user.id, bot.get_user(call.from_user.id).page.image)
        bot.send_message(call.from_user.id, "Для засвоєння матеріалу пройдіть короткий тест за темою лекції",
                         reply_markup=[bot.get_user(call.from_user.id).page.keyboard])
    elif call.data == "◀":
        bot.get_user(call.from_user.id).number -= 1
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id,
                                      reply_markup=[Lectures.get_keyboard(bot.get_user(call.from_user.id).number)])
    elif call.data == "▶":
        bot.get_user(call.from_user.id).number += 1
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id,
                                      reply_markup=[Lectures.get_keyboard(bot.get_user(call.from_user.id).number)])


@transliterate_function(language_code='ru', reversed=True)
def translate(text):
    return text.upper()


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
