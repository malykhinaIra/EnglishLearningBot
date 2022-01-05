from threading import Thread
from abc import abstractmethod
from telebot import *


class Game:
    """abstract class for game"""

    def __init__(self, bot, user_id):
        self.__difficulty = 'середня'
        self.__time = 3.
        self.__is_started = False
        self.__bot = bot
        self.__user_id = user_id
        self.__right_answer = ''
        self.__timer_thread = threading.Thread(self.timer())
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="почати", callback_data="start"))
        keyboard.add(types.InlineKeyboardButton(text="правила", callback_data="rules"))
        keyboard.add(types.InlineKeyboardButton(text="важкість: " + self.__difficulty, callback_data="difficulty"))
        # keyboard.add(types.InlineKeyboardButton(text="статистика", callback_data="statistics"))
        keyboard.add(types.InlineKeyboardButton(text="назад", callback_data="back"))
        self.__keyboard = keyboard

    def start(self):
        self.__is_started = True
        self.__right_answer = 'yes'
        self.__timer_thread.start()

    def timer(self):
        time_message = self.__bot.send_message(self.__user_id, f'лишилось {self.__time} хв')
        for half_of_minute in range(int(self.__time * 2), 1, -1):
            if not self.__is_started:
                return
            time_message.edit_text(self.__user_id, f'лишилось {float(half_of_minute) / 2} хв')
            time.sleep(30)
        self.exit(False)

    @abstractmethod
    def rules(self):
        pass

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
        self.__keyboard.keyboard.__getitem__(0).__getitem__(2).text = self.__difficulty

    # @classmethod
    # def get_statistics(cls):
    #     pass

    @abstractmethod
    def set_value(self):
        pass

    @abstractmethod
    def exit(self, is_win):
        if is_win:
            self.__bot.send_message(self.__user_id, 'Ти виграв!!!')
        else:
            self.__bot.send_message(self.__user_id, 'Час вийшов!!!')
            self.__bot.send_message(self.__user_id, f'Правильна відповідь: {self.__right_answer}')
        self.__is_started = False

    def get_keyboard(self):
        return self.__keyboard

    @property
    def is_started(self):
        return self.__is_started

    @property
    def time(self):
        return self.__time


class FirstLetterGame(Game):
    def __init__(self, **kwargs):
        pass

    def rules(self):
        return 'Ти отримуєш слово на аглійській мові і твоя задача перекласти його за певний час.'

    @classmethod
    def get_statistics(cls):
        pass

    def set_value(self):
        pass

    def exit(self, is_victory):
        pass


class TranslatorGame(Game):
    # time
    # reward
    def rules(self):
        pass

    @classmethod
    def get_statistics(cls):
        pass

    def set_value(self):
        pass

    def exit(self, is_victory):
        pass


class MixGame(Game):
    # time
    # reward

    def __init__(self, **kwargs):
        pass

    def rules(self):
        pass

    @classmethod
    def get_statistics(cls):
        pass

    def set_value(self):
        pass

    def exit(self, is_victory):
        pass


class PuzzleGame(Game):
    # time
    # reward

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def rules(self):
        pass

    @classmethod
    def get_statistics(cls):
        pass

    def set_value(self):
        pass

    def exit(self, is_victory):
        pass
