import random
import json
from Interfaces.ITest import ITest


def load_questions():
    with open("jsonFiles/tests.json", 'r', encoding="utf-8") as file:
        questions = json.load(file)
        return questions


class Test(ITest):
    def __init__(self, topic=None):
        self.topic = topic
        if not self.topic:
            self.topic = random.randint(1, 15)
        self.tests = load_questions()[str(self.topic)]
        self.list_test = list(self.tests.keys())
        self.questions = random.choice(self.list_test)
        self.variants = self.tests[self.questions]
        self.score = 0

    def passing_test(self, answer):
        if answer in self.variants:
            self.score += 1
            return f'Correct'
        else:
            return f'Wrong, correct answer is {self.variants[1]}'

    def __str__(self):
        return f' {self.questions}\n{self.variants[0]} '
