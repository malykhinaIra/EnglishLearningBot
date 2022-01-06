import json
from Interfaces.IPage import IPage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

with open("jsonFiles/lectures.json", 'r', encoding="utf-8") as file:
    data = json.load(file)


class Lectures(IPage):
    __keyboard = InlineKeyboardMarkup()
    __keyboard.add(InlineKeyboardButton(text='Дієслово (Verb)', callback_data='1'))
    __keyboard.add(InlineKeyboardButton(text='Герундій (Gerund)', callback_data='2'))
    __keyboard.add(InlineKeyboardButton(text='Інфінітив (Infinitive)', callback_data='3'))
    __keyboard.add(InlineKeyboardButton(text='Неправильні дієслова (Irregular Verbs)', callback_data='4'))
    __keyboard.add(InlineKeyboardButton(text='Фразові дієслова (Phrasal Verbs)', callback_data='5'))
    __keyboard.add(*[InlineKeyboardButton(name, callback_data=name) for name in ['◀', '▶']])

    def __init__(self, lecture=None):
        self.name = data[lecture]["name"]
        self.text = data[lecture]["text"]
        self.image = data[lecture]["image"]
        self.audio = None
        self.test = "test"
        self.index = int(lecture)

    def __str__(self):
        return f'\b{self.name}\b\n\n{self.text}'

    def exit(self):
        pass

    @classmethod
    def get_keyboard(cls):
        return cls.__keyboard
