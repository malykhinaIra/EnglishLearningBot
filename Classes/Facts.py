import random
import json
from typing import List


class Facts:
    def __init__(self):
        self.list_facts = load_facts()
        self.fact = random.choice(self.list_facts)

    def __str__(self):
        """Return a random fact from file"""
        return f' {self.fact} '


def load_facts() -> List[str]:
    """Deserialization of facts.json"""
    with open("JsonFiles/facts.json", 'r', encoding="utf-8") as file:
        fun_facts = json.load(file)
        return fun_facts
