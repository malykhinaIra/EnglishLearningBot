from abc import abstractmethod
from telebot import *
from Interfaces.IPage import IPage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class Game(IPage):
    """abstract class for game"""

    __keyboard = InlineKeyboardMarkup()
    __keyboard.add(InlineKeyboardButton(text="Слова", callback_data="words"))
    __keyboard.add(InlineKeyboardButton(text="Розшифруй слово", callback_data="cipher"))
    __keyboard.add(InlineKeyboardButton(text="Перекладач", callback_data="translate"))
    __keyboard.add(InlineKeyboardButton(text="Загадки", callback_data="riddles"))

    def __init__(self, bot, user_id):
        self.__difficulty = 'середня'
        self.__time = 3.
        self.__is_started = False
        self.__bot = bot
        self.__user_id = user_id
        self.__right_answer = ''
        self.__timer_thread = None
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="почати", callback_data="start"))
        keyboard.add(types.InlineKeyboardButton(text="правила", callback_data="rules"))
        self.__difficulty_keyboard = types.InlineKeyboardButton(text="важкість: " + self.__difficulty, \
                                                                callback_data="difficulty")
        keyboard.add(self.__difficulty_keyboard)
        # keyboard.add(types.InlineKeyboardButton(text="статистика", callback_data="statistics"))
        keyboard.add(types.InlineKeyboardButton(text="назад", callback_data="back"))
        self.__keyboard = keyboard

    def start(self):
        self.__is_started = True
        self.__right_answer = 'yes'
        self.__timer_thread = threading.Thread(self.timer())
        self.__timer_thread.start()

    def timer(self):
        time_message = self.__bot.send_message(self.__user_id, f'лишилось {self.__time} хв')
        for half_of_minute in range(int(self.__time * 2) - 1, 1, -1):
            time.sleep(30)
            if not self.__is_started:
                return
            self.__bot.edit_message_text(f'лишилось {float(half_of_minute) / 2} хв', \
                                         self.__user_id, time_message.message_id, )
        self.exit(False)

    def right_answer(self):
        return self.__right_answer

    def change_difficulty(self):
        if self.__difficulty == 'середня':
            self.__difficulty = 'важка'
            self.__time = 2
        else:
            if self.__difficulty == 'важка':
                self.__difficulty = 'легка'
                self.__time = 4.5
            else:
                self.__difficulty = 'середня'
                self.__time = 3
        self.__difficulty_keyboard.text = self.__difficulty

    # @classmethod
    # def get_statistics(cls):
    #     pass

    @abstractmethod
    def set_value(self):
        pass

    @abstractmethod
    def exit(self, is_win=False):
        self.__bot.send_message(self.__user_id, 'Гра завершена')
        if is_win:
            self.__bot.send_message(self.__user_id, 'Ти виграв!!!')
        else:
            self.__bot.send_message(self.__user_id, f'Правильна відповідь: {self.__right_answer}')
        self.__is_started = False

    @classmethod
    def get_keyboard(cls):
        return cls.__keyboard

    @property
    def keyboard(self):
        return self.__keyboard

    @property
    def is_started(self):
        return self.__is_started

    @property
    def time(self):
        return self.__time


class FirstLetterGame(Game):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return 'Ти отримуєш слово на аглійській мові і твоя задача перекласти його за певний час.'

    @classmethod
    def get_statistics(cls):
        pass

    def set_value(self):
        pass

    def exit(self, is_victory=False):
        pass


class TranslatorGame(Game):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        pass

    @classmethod
    def get_statistics(cls):
        pass

    def set_value(self):
        pass

    def exit(self, is_victory=False):
        pass


class MixGame(Game):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        pass

    @classmethod
    def get_statistics(cls):
        pass

    def set_value(self):
        pass

    def exit(self, is_victory=False):
        pass


class PuzzleGame(Game):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        pass

    @classmethod
    def get_statistics(cls):
        pass

    def set_value(self):
        pass

    def exit(self, is_victory=False):
        pass
