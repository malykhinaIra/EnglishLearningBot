import random
import json

from Classes.constants import test_start_time
from Interfaces.ITest import ITest
from aiogram.types import InlineKeyboardMarkup
from Classes.Timer import Timer
from telebot import TeleBot
from keyboards import TestKeyboard
from typing import List, Dict


def load_questions() -> Dict[str, Dict[str, List[str]]]:
    """Deserialization of tests.json"""
    with open("jsonFiles/tests.json", 'r', encoding="utf-8") as file:
        questions = json.load(file)
        return questions


class Test(ITest):
    __keyboard = TestKeyboard.keyboard

    def __init__(self, bot: TeleBot, user_id: int, topic: int = 0):
        """Class for pass test"""
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
            self.__questions = list(self.__test.keys())
        else:
            tests = load_questions()
            self.__test = dict()
            for test in tests.values():
                for question in test:
                    self.__test[question] = test[question]
            self.__questions = list(self.__test.keys())
        self.__score = 0
        self.__unused_question = self.__questions
        self.__current_question = None
        self.__past_question = None
        self.__timer = Timer(bot, user_id)
        self.__time_message = None
        self.__timer.add_end_action(self.__end)
        self.__timer.add_update_action(self.__update)
        self.start()

    def next_task(self):
        """Do the next question"""
        if self.__unused_question:
            self.__current_question = random.choice(self.__unused_question)
            self.__unused_question.remove(self.__current_question)

    def passing_test(self, answer: str) -> str:
        """Return result (answer correct or not), count user's score"""
        right_answer = self.__test[self.__current_question][1]
        self.__past_question = self.__current_question
        self.__current_question = None
        if answer == right_answer:
            self.__score += 1
            return f'Correct'
        return f'Wrong, correct answer is {right_answer}'

    def __str__(self):
        """Return questions with answer options"""
        if not self.__current_question:
            raise ValueError('there are no task')
        return f' {self.__current_question}\n{self.__test[self.__current_question][0]} '

    @classmethod
    def get_keyboard(cls) -> InlineKeyboardMarkup:
        """Get keyboard with button to start the test"""
        return cls.__keyboard

    @property
    def index(self) -> int:
        return self.__index

    @property
    def score(self) -> int:
        """Get score of passing test"""
        return self.__score

    @property
    def sentence(self) -> str:
        return self.__current_question

    @property
    def last_sentence(self) -> str:
        return self.__past_question

    @property
    def is_started(self) -> bool:
        return self.__timer.is_started

    def delete(self):
        """Delete timer-message"""
        if self.__timer.is_started:
            self.stop()
        del self

    def start(self):
        """Starts the timer"""
        self.next_task()
        self.stop()
        self.__time_message = self.__bot.send_message(self.__user_id, 'Залишилось 10 хв')
        self.__timer.start(test_start_time)

    def __end(self):
        """Send message if time run out"""
        self.__bot.send_message(self.__user_id, f'Час вийшов')
        self.__bot.delete_message(self.__user_id, self.__time_message.message_id)
        self.__time_message = None
        self.__bot.send_message(self.__user_id, "Новий тест", reply_markup=[Test.get_keyboard()])

    def __update(self, minutes):
        """Updating of timer"""
        if not minutes:
            self.__bot.edit_message_text('Залишилось менше 30 секунд', self.__user_id, self.__time_message.message_id)
        else:
            self.__bot.edit_message_text(
                f'Залишил{"a" if int(minutes * 2) == 3 else "o"}сь {minutes} хв',
                self.__user_id, self.__time_message.message_id)

    def stop(self):
        """Stop the timer"""
        if self.__timer.is_started:
            self.__bot.delete_message(self.__user_id, self.__time_message.message_id)
            self.__time_message = None
            self.__timer.stop()
