import json
import random
from Interfaces.IRecomendations import IRecomendations


class Book(IRecomendations):
    def __init__(self, level: str):
        """Class for return random book"""
        self.books = load_books()
        self.level = level
        self.list_chose = list(self.books[self.level].keys())
        self.name_book = self.books[self.level][random.choice(self.list_chose)]

    @property
    def level(self):
        """Get the level of english."""
        return self._level

    @level.setter
    def level(self, level):
        """Set the level of english."""
        if not isinstance(level, str):
            raise TypeError('level should have type "str"')
        self._level = level

    def image(self) -> str:
        """Get the url on cover of book."""
        return self.name_book["image"]

    def description(self) -> str:
        """Get the description of book."""
        return f'Level: {self.level}\n\t{self.name_book["name"]}\n{self.name_book["description"]}'


class Film(IRecomendations):
    def __init__(self, level):
        """Class for return random film"""
        self.films = load_films()
        self.level = level
        self.list_chose = list(self.films[self.level].keys())
        self.name_film = self.films[self.level][random.choice(self.list_chose)]

    @property
    def level(self):
        """Get the level of english."""
        return self._level

    @level.setter
    def level(self, level):
        """Set the level of english."""
        if not isinstance(level, str):
            raise TypeError('level should have type "str"')
        self._level = level

    def description(self):
        """Get the description of book."""
        return f'Level: {self.level}\n\t{self.name_film["name"]}\n{self.name_film["description"]}'

    def image(self):
        """Get the url on poster of film."""
        return self.name_film["image"]


def get_recommend(choose, level):
    """Factory function for return information about film or book """
    dict_recommend = {"film": Film(level), "book": Book(level)}
    return dict_recommend[choose]


def load_books() -> dict:
    """Deserialization of books.json"""
    with open("jsonFiles/books.json", "r", encoding="utf8") as file:
        books = json.load(file)
        return books


def load_films() -> dict:
    """Deserialization of films.json"""
    with open("jsonFiles/films.json", "r", encoding="utf8") as films:
        films = json.load(films)
        return films
