import json
from random import choice, randint
from abc import abstractmethod
from telebot import *
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Classes.Timer import Timer
from Classes.Words import Words
from keyboards import GameKeyboard
from typing import List
from types import LambdaType


class Game:
    """Abstract class for game"""

    __keyboard = GameKeyboard.keyboard

    def __init__(self, bot: TeleBot, user_id: int, game_name: str, rules: List[LambdaType]):
        if not isinstance(user_id, int):
            raise TypeError('user_id should have type "int"')
        if not isinstance(rules, list):
            raise TypeError('rules should be list')
        for element in rules:
            if not isinstance(element, LambdaType):
                raise ValueError('every element of rules should be function')
        if not isinstance(game_name, str):
            raise TypeError('game_name should have type "str"')
        if not isinstance(bot, TeleBot):
            raise TypeError('bot should have type "TeleBot"')
        self.__rules = rules
        self._difficulty = 'середня'
        self.__time = 3
        self._bot = bot
        self._user_id = user_id
        self._right_answer = ''
        self.__timer = Timer(self._bot, self._user_id)
        self.__timer.add_end_action(self.__end)
        self.__timer.add_update_action(self.__update)
        self.__game_name = game_name
        self.__keyboard = InlineKeyboardMarkup()
        self.__keyboard.add(InlineKeyboardButton(text="Старт", callback_data="start"))
        self.__keyboard.add(InlineKeyboardButton(text="Правила", callback_data="rules"))
        self.__keyboard.add(InlineKeyboardButton(text="Важкість: " + self._difficulty,
                                                 callback_data="difficulty"))
        self.__keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back"))
        self.__menu_message = bot.send_message(self._user_id, 'Меню гри: ' + game_name, reply_markup=[self.__keyboard])
        self.__time_message = None

    def _start(self, right_answer: str = None):
        """Function to start the timer"""
        if not isinstance(right_answer, str):
            raise TypeError('right_answer should have type "str"')
        self.stop()
        self._right_answer = right_answer
        self.__time_message = self._bot.send_message(self._user_id,
                                                     'Залишил' + ("a" if int(self.__time * 2) == 2 else "o") +
                                                     'сь ' + str(self.__time) + ' хв')
        self.__timer.start(self.__time)

    def change_difficulty(self):
        """Function to set difficulty of the game"""
        if self._difficulty == 'середня':
            self._difficulty = 'важка'
            self.__time = 2.
        else:
            if self._difficulty == 'важка':
                self._difficulty = 'легка'
                self.__time = 4.5
            else:
                self._difficulty = 'середня'
                self.__time = 3.
        self.__keyboard = InlineKeyboardMarkup()
        self.__keyboard.add(InlineKeyboardButton(text="Start", callback_data="start"))
        self.__keyboard.add(InlineKeyboardButton(text="Правила", callback_data="rules"))
        self.__keyboard.add(InlineKeyboardButton(text="Важкість: " + self._difficulty,
                                                 callback_data="difficulty"))
        self.__keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back"))
        self._bot.edit_message_text(message_id=self.__menu_message.id, chat_id=self._user_id,
                                    reply_markup=[self.__keyboard], text=self.__menu_message.text)

    @abstractmethod
    def __str__(self):
        pass

    def _set_value_into_rules(self, **kwargs):
        self.__values_for_rules = kwargs

    def set_answer(self, value: str):
        """Function to get answer from user"""
        if not isinstance(value, str):
            raise TypeError('value should have type "str"')
        value = value.lower()
        for element in self.__rules:
            if not element(value, **self.__values_for_rules):
                return False
        return True

    def __update(self, minutes: float or int):
        """Update timer of game"""
        if minutes == 0:
            self._bot.edit_message_text('Залишилось менше 30 секунд', self._user_id, self.__time_message.message_id)
        else:
            self._bot.edit_message_text(
                f'Залишил{"a" if int(minutes * 2) == 3 else "o"}сь {minutes} хв',
                self._user_id, self.__time_message.message_id)

    def __end(self):
        """End game if no answer and time run out"""
        self._bot.delete_message(self._user_id, self.__time_message.message_id)
        self.__time_message = None
        self._bot.send_message(self._user_id, f'Час вийшов')
        if self._right_answer:
            self._bot.send_message(self._user_id, f'Правильна відповідь: {self._right_answer}')
        self.__menu_message = self._bot.send_message(self._user_id, 'Меню гри: ' + self.__game_name,
                                                     reply_markup=[self.__keyboard])

    def stop(self, is_win: bool = False):
        """Function to stop the game and timer"""
        if not isinstance(is_win, bool):
            raise TypeError('is_win should have type "bool"')
        if self.__timer.is_started:
            if is_win:
                self._bot.send_message(self._user_id, 'Ти виграв!!!')
            else:
                self._bot.send_message(self._user_id, f'Гра завершена')
                self._bot.send_message(self._user_id, f'Правильна відповідь: {self._right_answer}')
            self._bot.delete_message(self._user_id, self.__time_message.message_id)
            self.__time_message = None
            self.__menu_message = self._bot.send_message(self._user_id, 'Меню гри: ' + self.__game_name,
                                                         reply_markup=[self.__keyboard])
            self.__timer.stop()

    def delete(self):
        """Delete timer-message"""
        if self.__timer.is_started:
            self.stop()
        del self

    @classmethod
    def get_keyboard(cls) -> InlineKeyboardMarkup:
        """Get keyboard with list of games"""
        return cls.__keyboard

    @property
    def right_answer(self) -> str:
        return self._right_answer

    @property
    def keyboard(self) -> InlineKeyboardMarkup:
        """Get keyboard with game's menu"""
        return self.__keyboard

    @property
    def is_started(self) -> bool:
        return self.__timer.is_started

    @property
    def time(self) -> int:
        return self.__time

    @property
    def difficulty(self) -> str:
        return self._difficulty


class TranslatorGame(Game):
    def __init__(self, *args):
        """Class for game "Translator" """
        super().__init__(*args, game_name='Перекладач', rules=[lambda word_l, **kwargs: word_l == kwargs['word']])

    def __str__(self):
        """Rules of the game"""
        return 'Ти отримуєш слово - твоє завдання перекласти його.'

    def start(self):
        """Function to start the game"""
        words = Words.read_words()
        word = words[randint(0, len(words))]
        self._bot.send_message(self._user_id, f'Слово: {word[1]}')
        right_answer = word[0]
        super()._set_value_into_rules(word=word[0])
        self._start(right_answer)


class MixGame(Game):
    def __init__(self, *args):
        """Class for game "Mix" """
        super().__init__(*args, game_name='Мішанина', rules=[lambda value, **kwargs: value == kwargs['word']])

    def __str__(self):
        """Rules of the game"""
        return 'Ти отримуєш перемішані букви - твоє завдання зрозуміти слово.'

    def start(self):
        words = Words.read_words()
        word = words[randint(0, len(words) - 1)]
        length = len(word[0])
        while not MixGame.__is_in_range(length, self._difficulty):
            word = words[randint(0, len(words) - 1)]
            length = len(word[0])
        mix = ''
        super()._set_value_into_rules(word=word[0])
        while True:
            is_used = [False for i in range(length)]
            while not length == len(mix):
                index = randint(0, length - 1)
                if not is_used[index]:
                    mix += word[0][index]
                    is_used[index] = True
            if not super().set_answer(mix):
                break
            mix = ''
        self._bot.send_message(self._user_id, f'Слово: {mix}')
        self._start(word[0])

    @staticmethod
    def __is_in_range(number: int, difficulty: str) -> bool:
        if difficulty == 'легка':
            return number <= 6
        elif difficulty == 'середня':
            return 3 <= number <= 8
        return 6 <= number <= 11


class PuzzleGame(Game):
    def __init__(self, *args):
        """Class for game "Puzzle" """
        self.__game_count = 0
        self.__used_riddles = set()
        super().__init__(*args, game_name='Загадки', rules=[lambda value, **kwargs: value == kwargs['word']])

    def __str__(self):
        """Rules of the game"""
        return 'Ти отримуєш загадку - твоє завдання розгадати її, написавши слово-відповідь.'

    def start(self, is_first_time: bool = True):
        """Function to start the game"""
        if not isinstance(is_first_time, bool):
            raise TypeError('is_first_time should have type "bool"')
        with open('jsonFiles/riddles.json', 'r') as file:
            riddles = json.loads(file.read())
            riddle = choice(list(riddles.keys()))
            while riddle in self.__used_riddles:
                riddle = choice(list(riddles.keys()))
            self.__used_riddles.add(riddle)
            self._bot.send_message(self._user_id, f'Загадка: {riddle}')
            super()._set_value_into_rules(word=riddles[riddle])
            if is_first_time:
                self.__game_count = {'легка': 1, 'середня': 2, 'важка': 3}[self._difficulty]
                self._start(riddles[riddle])

    def stop(self, is_win: bool = False):
        """Function to stop the game"""
        if not isinstance(is_win, bool):
            raise TypeError('is_win should have type "bool"')
        if is_win:
            self._bot.send_message(self._user_id, 'Правильно')
            self.__game_count -= 1
            if self.__game_count:
                self.start(False)
            else:
                super().stop(True)
        else:
            super().stop()
