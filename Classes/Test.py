import random
import json
from Interfaces.ITest import ITest
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def load_questions():
    with open("jsonFiles/tests.json", 'r', encoding="utf-8") as file:
        questions = json.load(file)
        return questions


class Test(ITest):
    __keyboard = InlineKeyboardMarkup()
    __keyboard.add(InlineKeyboardButton(text='Розпочати', callback_data='tests'))

    def __init__(self, topic=random.randint(1, 15)):
        self.__index = topic
        self.__test = load_questions()[str(self.__index)]
        self.__sentences = list(self.__test.keys())
        self.__score = 0
        self.__unused_sentences = self.__sentences
        self.__current_sentence = None
        self.next_task()

    def next_task(self):
        if self.__unused_sentences:
            self.__current_sentence = random.choice(self.__unused_sentences)
            self.__unused_sentences.remove(self.__current_sentence)

    def passing_test(self, answer):
        if not self.__current_sentence:
            raise ValueError('there are no task to answer')
        right_answer = self.__test[self.__current_sentence][1]
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
    def get_keyboard(cls):
        return cls.__keyboard

    @property
    def score(self):
        return self.__score

    @property
    def sentence(self):
        return self.__current_sentence
