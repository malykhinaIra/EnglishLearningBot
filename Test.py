import random


class Test:
    def __init__(self):
        self.tests = ["Random test 1", "Random test 2"]
        self.test = self.tests[random.randint(0, len(self.tests) - 1)]

    def __str__(self):
        return f'{self.test}'
