import json
import random
from PIL import Image


class Book():
    def __init__(self, level):
        with open("books.json","r", encoding="utf8") as books:
          self.books = json.load(books)
        self.level = level
        self.list_choise = list(self.books[self.level].keys())
        self.name_book = self.books[self.level][random.choice(self.list_choise)]

    def image(self):
        return self.name_book["image"]

    def description(self):
        return f'Level: {self.level}\n\t{self.name_book["name"]}\n{self.name_book["description"]}'


class Film():
    def __init__(self, level):
        with open("films.json", "r", encoding="utf8") as films:
         self.films = json.load(films)
        self.level = level
        self.list_choise = list(self.films[self.level].keys())
        self.name_film = self.films[self.level][random.choice(self.list_choise)]

    def description(self):
        return f'Level: {self.level}\n\t{self.name_film["name"]}\n{self.name_film["description"]}'

    def image(self):
        return self.name_film["image"]


def get_recommend(choose, level):
    dict_recommend = {"film": Film(level), "book": Book(level)}
    return dict_recommend[choose]


