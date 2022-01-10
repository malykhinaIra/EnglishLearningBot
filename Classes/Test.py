import random
import json
from Interfaces.ITest import ITest
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Classes.Timer import Timer
from telebot import TeleBot
from typing import List, Dict


def load_questions() -> Dict[str, Dict[str, List[str]]]:
    with open("jsonFiles/tests.json", 'r', encoding="utf-8") as file:
        questions = json.load(file)
        return questions


class Test(ITest):
    __keyboard = InlineKeyboardMarkup()
    __keyboard.add(InlineKeyboardButton(text='Розпочати', callback_data='tests'))

    def __init__(self, bot: TeleBot, user_id: int, topic: int = 0):
        if not isinstance(user_id, int):
            raise TypeError('user_id should have type "int"')
        if not isinstance(topic, int):
            raise TypeError('topic should have type "int"')
        if not isinstance(bot, TeleBot):
            raise TypeError('bot should have type "TeleBot"')
        self.__bot = bot
        self.__user_id = user_id
        self.__index = topic
        if topic:
            self.__test = load_questions()[str(self.__index)]
            self.__sentences = list(self.__test.keys())
        else:
            tests = load_questions()
            self.__test = dict()
            for test in tests.values():
                for question in test:
                    self.__test[question] = test[question]
            self.__sentences = list(self.__test.keys())
        self.__score = 0
        self.__unused_sentences = self.__sentences
        self.__current_sentence = None
        self.__past_sentence = None
        self.__timer = Timer(bot, user_id)
        self.__time_message = None
        self.__timer.add_end_action(self.__end)
        self.__timer.add_update_action(self.__update)
        self.start()

    def next_task(self):
        if self.__unused_sentences:
            self.__current_sentence = random.choice(self.__unused_sentences)
            self.__unused_sentences.remove(self.__current_sentence)

    def is_right(self, answer: str) -> bool:
        if not isinstance(answer, str):
            raise TypeError('answer should have type "str"')
        return self.__test[self.__current_sentence][1] == answer

    def passing_test(self, answer: str) -> str:
        if not self.__current_sentence:
            raise ValueError('there are no task to answer')
        right_answer = self.__test[self.__current_sentence][1]
        self.__past_sentence = self.__current_sentence
        self.__current_sentence = None
        if answer == right_answer:
            self.__score += 1
            return f'Correct'
        return f'Wrong, correct answer is {right_answer}'

    def __str__(self):
        if not self.__current_sentence:
            raise ValueError('there are no task')
        return f' {self.__current_sentence}\n{self.__test[self.__current_sentence][0]} '

    @classmethod
    def get_keyboard(cls) -> InlineKeyboardMarkup:
        return cls.__keyboard

    @property
    def index(self) -> int:
        return self.__index

    @property
    def score(self) -> int:
        return self.__score

    @property
    def questions_count(self):
        return len(self.__sentences)

    @property
    def sentence(self) -> str:
        return self.__current_sentence

    @property
    def last_sentence(self) -> str:
        return self.__past_sentence

    @property
    def is_started(self) -> bool:
        return self.__timer.is_started

    def delete(self):
        if self.__timer.is_started:
            self.stop()
        del self

    def start(self):
        self.next_task()
        self.stop()
        self.__time_message = self.__bot.send_message(self.__user_id, 'Лишилось 10 хв')
        self.__timer.start(10)

    def __end(self):
        self.__bot.send_message(self.__user_id, f'Час вийшов')
        self.__bot.delete_message(self.__user_id, self.__time_message.message_id)
        self.__time_message = None
        self.__bot.send_message(self.__user_id, "Новий тест", reply_markup=[Test.get_keyboard()])

    def __update(self, minutes):
        if minutes == 0:
            self.__bot.edit_message_text('Лишилось менше 30 секунд', self.__user_id, self.__time_message.message_id)
        else:
            self.__bot.edit_message_text(
                f'лишил{"a" if int(minutes * 2) == 3 else "o"}сь {minutes} хв',
                self.__user_id, self.__time_message.message_id)

    def stop(self):
        if self.__timer.is_started:
            self.__bot.delete_message(self.__user_id, self.__time_message.message_id)
            self.__time_message = None
            self.__timer.stop()
