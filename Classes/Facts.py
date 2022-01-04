import random
import json

def load_facts():
    with open("jsonFiles/facts.json", 'r', encoding="utf-8") as file:
        fun_facts = json.load(file)
        return fun_facts


class Facts:
    def __init__(self):
        self.list_facts = load_facts()
        self.fact = random.choice(self.list_facts)

    def __str__(self):
        return f' {self.fact} '
