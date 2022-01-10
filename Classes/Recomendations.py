import json
import random
from Interfaces.IRecomendations import IRecomendations


class Book(IRecomendations):
    def __init__(self, level: str):
        if not isinstance(level, str):
            raise TypeError('level should have type "str"')
        with open("jsonFiles/books.json", "r", encoding="utf8") as books:
            self.books = json.load(books)
        self.__level = level
        self.__list_chose = list(self.books[self.__level].keys())
        self.__name_book = self.books[self.__level][random.choice(self.__list_chose)]

    def image(self) -> str:
        return self.__name_book["image"]

    def description(self) -> str:
        return f'Level: {self.__level}\n\t{self.__name_book["name"]}\n{self.__name_book["description"]}'


class Film(IRecomendations):
    def __init__(self, level):
        with open("jsonFiles/films.json", "r", encoding="utf8") as films:
            self.films = json.load(films)
        self.level = level
        self.list_chose = list(self.films[self.level].keys())
        self.name_film = self.films[self.level][random.choice(self.list_chose)]

    def description(self):
        return f'Level: {self.level}\n\t{self.name_film["name"]}\n{self.name_film["description"]}'

    def image(self):
        return self.name_film["image"]


def get_recommend(choose, level):
    dict_recommend = {"film": Film(level), "book": Book(level)}
    return dict_recommend[choose]
