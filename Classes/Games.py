from abc import abstractmethod
from telebot import *
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Classes.Timer import Timer


class Game:
    """abstract class for game"""

    __keyboard = InlineKeyboardMarkup()
    __keyboard.add(InlineKeyboardButton(text="Перша буква", callback_data="words"))
    __keyboard.add(InlineKeyboardButton(text="Мішанина", callback_data="cipher"))
    __keyboard.add(InlineKeyboardButton(text="Перекладач", callback_data="translate"))
    __keyboard.add(InlineKeyboardButton(text="Загадки", callback_data="riddles"))

    def __init__(self, bot, user_id, game_name):
        if not isinstance(user_id, int):
            raise TypeError('user_id should have type "int"')
        if not isinstance(game_name, str):
            raise TypeError('game_name should have type "str"')
        if not isinstance(bot, TeleBot):
            raise TypeError('bot should have type "TeleBot"')
        self.__difficulty = 'середня'
        self.__time = 3.
        self.__bot = bot
        self.__user_id = user_id
        self.__right_answer = 'yes'
        self.__timer = Timer(self.__bot, self.__user_id)
        self.__timer.add_end_action(self.__end)
        self.__game_name = game_name
        self.__keyboard = InlineKeyboardMarkup()
        self.__keyboard.add(InlineKeyboardButton(text="почати", callback_data="start"))
        self.__keyboard.add(InlineKeyboardButton(text="правила", callback_data="rules"))
        self.__keyboard.add(InlineKeyboardButton(text="важкість: " + self.__difficulty, \
                                                 callback_data="difficulty"))
        # keyboard.add(types.InlineKeyboardButton(text="статистика", callback_data="statistics"))
        self.__keyboard.add(InlineKeyboardButton(text="назад", callback_data="back"))
        self.__menu_message = bot.send_message(self.__user_id, 'меню гри: ' + game_name, reply_markup=[self.__keyboard])

    def start(self):
        self.__timer.start(self.__time)

    @property
    def right_answer(self):
        return self.__right_answer

    def change_difficulty(self):
        if self.__difficulty == 'середня':
            self.__difficulty = 'важка'
            self.__time = 2.
        else:
            if self.__difficulty == 'важка':
                self.__difficulty = 'легка'
                self.__time = 4.5
            else:
                self.__difficulty = 'середня'
                self.__time = 3.
        self.__keyboard = InlineKeyboardMarkup()
        self.__keyboard.add(InlineKeyboardButton(text="почати", callback_data="start"))
        self.__keyboard.add(InlineKeyboardButton(text="правила", callback_data="rules"))
        self.__keyboard.add(InlineKeyboardButton(text="важкість: " + self.__difficulty, \
                                                 callback_data="difficulty"))
        # keyboard.add(types.InlineKeyboardButton(text="статистика", callback_data="statistics"))
        self.__keyboard.add(InlineKeyboardButton(text="назад", callback_data="back"))
        self.__bot.edit_message_text(message_id=self.__menu_message.id, chat_id=self.__user_id, \
                                     reply_markup=[self.__keyboard], text=self.__menu_message.text)

    # @classmethod
    # def get_statistics(cls):
    #     pass

    @abstractmethod
    def set_value(self):
        pass

    def __end(self):
        self.__bot.send_message(self.__user_id, f'Час вийшов')
        self.__bot.send_message(self.__user_id, f'Правильна відповідь: {self.__right_answer}')
        self.__menu_message = self.__bot.send_message(self.__user_id, 'меню гри: ' + self.__game_name,
                                                      reply_markup=[self.__keyboard])

    def stop(self, is_win=False):
        if is_win:
            self.__bot.send_message(self.__user_id, 'Ти виграв!!!')
            self.__menu_message = self.__bot.send_message(self.__user_id, 'меню гри: ' + self.__game_name,
                                                          reply_markup=[self.__keyboard])
        self.__timer.stop()

    def __del__(self):
        if self.__timer.is_started:
            self.__timer.stop()

    @classmethod
    def get_keyboard(cls):
        return cls.__keyboard

    @property
    def keyboard(self):
        return self.__keyboard

    @property
    def is_started(self):
        return self.__timer.is_started

    @property
    def time(self):
        return self.__time


class FirstLetterGame(Game):
    def __init__(self, *args):
        super().__init__(*args, game_name='Перша буква')

    def __str__(self):
        return 'Ти отримуєш слово на аглійській мові і твоя задача перекласти його за певний час.'

    @classmethod
    def get_statistics(cls):
        pass

    def set_value(self):
        pass


class TranslatorGame(Game):
    def __init__(self, *args):
        super().__init__(*args, game_name='Перекладач')

    def __str__(self):
        pass

    @classmethod
    def get_statistics(cls):
        pass

    def set_value(self):
        pass


class MixGame(Game):
    def __init__(self, *args):
        super().__init__(*args, game_name='Мішанина')

    def __str__(self):
        pass

    @classmethod
    def get_statistics(cls):
        pass

    def set_value(self):
        pass


class PuzzleGame(Game):
    def __init__(self, *args):
        super().__init__(*args, game_name='Загадки')

    def __str__(self):
        pass

    @classmethod
    def get_statistics(cls):
        pass

    def set_value(self):
        pass
