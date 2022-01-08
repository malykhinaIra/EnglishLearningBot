import ctypes
import random
from abc import abstractmethod
from telebot import *
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Classes.Timer import Timer
from ctypes import c_char
from Classes.Words import Words


class Game:
    """abstract class for game"""

    __keyboard = InlineKeyboardMarkup()
    __keyboard.add(InlineKeyboardButton(text="Перша буква", callback_data="words"))
    __keyboard.add(InlineKeyboardButton(text="Мішанина", callback_data="cipher"))
    __keyboard.add(InlineKeyboardButton(text="Перекладач", callback_data="translate"))
    __keyboard.add(InlineKeyboardButton(text="Загадки", callback_data="riddles"))

    def __init__(self, bot, user_id, game_name, is_right_answer):
        if not isinstance(user_id, int):
            raise TypeError('user_id should have type "int"')
        if not isinstance(is_right_answer, Callable):
            raise TypeError('is_right_answer should be callable')
        if not isinstance(game_name, str):
            raise TypeError('game_name should have type "str"')
        # if not isinstance(right_answer, str):
        #     raise TypeError('right_answer should have type "str"')
        if not isinstance(bot, TeleBot):
            raise TypeError('bot should have type "TeleBot"')
        self.__difficulty = 'середня'
        self.__time = 3.
        self._bot = bot
        self._user_id = user_id
        self.__is_right_answer = is_right_answer
        # self.__right_answer = right_answer
        self.__right_answer = ''
        self.__timer = Timer(self._bot, self._user_id)
        self.__timer.add_end_action(self.__end)
        self.__game_name = game_name
        self.__keyboard = InlineKeyboardMarkup()
        self.__keyboard.add(InlineKeyboardButton(text="почати", callback_data="start"))
        self.__keyboard.add(InlineKeyboardButton(text="правила", callback_data="rules"))
        self.__keyboard.add(InlineKeyboardButton(text="важкість: " + self.__difficulty, \
                                                 callback_data="difficulty"))
        # keyboard.add(types.InlineKeyboardButton(text="статистика", callback_data="statistics"))
        self.__keyboard.add(InlineKeyboardButton(text="назад", callback_data="back"))
        self.__menu_message = bot.send_message(self._user_id, 'меню гри: ' + game_name, reply_markup=[self.__keyboard])

    def start(self, right_answer):
        if not isinstance(right_answer, str):
            raise TypeError('right_answer should have type "str"')
        self.__right_answer = right_answer
        self.__timer.start(self.__time)

    def right_answer(self):
        if not self.is_started:
            raise ValueError('game has not started yet')
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
        self._bot.edit_message_text(message_id=self.__menu_message.id, chat_id=self._user_id, \
                                    reply_markup=[self.__keyboard], text=self.__menu_message.text)

    # @classmethod
    # def get_statistics(cls):
    #     pass

    @abstractmethod
    def __str__(self):
        pass

    def set_answer(self, value: str):
        if not isinstance(value, str):
            raise TypeError('value should have type "str"')
        return self.__is_right_answer(value)

    def __end(self):
        self._bot.send_message(self._user_id, f'Час вийшов')
        self._bot.send_message(self._user_id, f'Правильна відповідь: {self.__right_answer}')
        self.__menu_message = self._bot.send_message(self._user_id, 'меню гри: ' + self.__game_name,
                                                     reply_markup=[self.__keyboard])

    def stop(self, is_win=False):
        if is_win:
            self._bot.send_message(self._user_id, 'Ти виграв!!!')
            self.__menu_message = self._bot.send_message(self._user_id, 'меню гри: ' + self.__game_name,
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
        self.__right_answer = ''
        self.__condition = set()
        super().__init__(*args, game_name='Перша буква', is_right_answer=self.__is_right_answer)

    def __str__(self):
        return 'Ти отримуєш букву і твоє завдання написати слово, що починається на цю буквую'

    # @classmethod
    # def get_statistics(cls):
    #     pass

    def start(self):
        letter = chr(random.randint(97, 122))
        self._bot.send_message(self._user_id, f'Буква: {letter}')
        condition = lambda word: True if re.match(f'^{letter}[a-zA-Z]*$', word) else False
        for element in Words.read_words():
            if condition(element[0]):
                self.__right_answer = element[0]
                break
        self.__condition.add(lambda word: True if Words.read_word(word) else False)
        self.__condition.add(condition)
        super().start(self.__right_answer)

    def __is_right_answer(self, value):
        for condition in self.__condition:
            if not condition(value):
                return False
        return True


class TranslatorGame(Game):
    def __init__(self, *args):
        self.__right_answer = ''
        self.__condition = set()
        super().__init__(*args, game_name='Перекладач', is_right_answer=self.__is_right_answer)

    def __str__(self):
        return 'Ти отримуєш слово на аглійській мові і твоя задача перекласти його.'

    # @classmethod
    # def get_statistics(cls):
    #     pass

    def start(self):
        words = Words.read_words()
        word = words[random.randint(0, len(words))]
        self._bot.send_message(self._user_id, f'Слово: {word[1]}')
        self.__right_answer = word[0]
        self.__condition.add(lambda word_l: word_l == word[0])
        super().start(self.__right_answer)

    def __is_right_answer(self, value):
        for condition in self.__condition:
            if not condition(value):
                return False
        return True


class MixGame(Game):
    def __init__(self, *args):
        self.__right_answer = ''
        self.__condition = set()
        super().__init__(*args, game_name='Мішанина', is_right_answer=self.__is_right_answer)

    def __str__(self):
        return 'Ти отримуєш перемішані букви і твоя задача зрозуміти слово.'

        # @classmethod
        # def get_statistics(cls):
        #     pass

    def start(self):
        words = Words.read_words()
        word = words[random.randint(0, len(words))]
        mix = ''
        length = len(word[0])
        is_used = [False for i in range(length)]
        while not length == len(mix):
            index = random.randint(0, length)
            if not is_used[index]:
                mix += word[0][index]
                is_used[index] = True
        self._bot.send_message(self._user_id, f'Слово: {mix}')
        self.__right_answer = word[0]
        self.__condition.add(lambda word_l: word_l == word[0])
        super().start(self.__right_answer)

    def __is_right_answer(self, value):
        for condition in self.__condition:
            if not condition(value):
                return False
        return True


class PuzzleGame(Game):
    def __init__(self, *args):
        self.__right_answer = ''
        self.__condition = set()
        super().__init__(*args, game_name='Загадки', is_right_answer=self.__is_right_answer)

    def __str__(self):
        return 'Ти отримуєш слово на аглійській мові і твоя задача перекласти його.'

        # @classmethod
        # def get_statistics(cls):
        #     pass

    def start(self):
        words = Words.read_words()
        word = words[random.randint(0, len(words))]
        self._bot.send_message(self._user_id, f'Слово: {word[1]}')
        self.__right_answer = word[0]
        self.__condition.add(lambda word_l: word_l == word[0])
        super().start(self.__right_answer)

    def __is_right_answer(self, value):
        for condition in self.__condition:
            if not condition(value):
                return False
        return True
