import json
import random
from PIL import Image

class Book():
    def __init__(self,level):
        with open("books.json", "r") as books:
          self.books = json.load(books)
        self.level = level
        self.list_choise = list(self.books[self.level].keys())
        self.name_book = self.books[self.level][random.choice(self.list_choise)]

    def image_book(self):
        im = Image.open(self.books["image"])
        return im.show()

    def random_book(self):
        return f'{self.name_book["name"]}\n{self.name_book["description"]}'


class Film():
    def __init__(self,level):
        with open("films.json", "r") as films:
          self.films = json.load(films)
        self.level = level
        self.list_choise = list(self.films[self.level].keys())
        self.name_film = self.films[self.level][random.choice(self.list_choise)]

    def random_film(self):
        return f'{self.name_film["name"]}\n{self.name_film["description"]}'

    def image_film(self):
        im = Image.open(self.films["image"])
        return im.show()


class Recomendations:
    def __init__(self, level):
        self.level = level
        self.book = Book(self.level)
        self.film = Film(self.level)

    def __str__(self):
        return f'For {self.level}:\n Book: {self.book.random_book()};\n Film: {self.film.random_film()}'




#
# films = {
#     "A1": {
#         "Film1": {
#             "name": "The Jungle Book (Книга Джунглів) ",
#             "image": "images\\film1.png",
#             "description": "Оne of the best cartoons of the legendary Disney studio. If you are just starting to learn"
#                            "English, we advise you to remember the wonderful tale of Mowgli and improve your language "
#                            "skills."
#         },
#         "Film2": {
#             "name": "Up (Вгору)",
#             "image": "images\\film2.png",
#             "description": "Сute and exciting story in the Pixar studio cartoon about a jungle trip in a balloon is "
#                            "perfect for the A1 level."
#         },
#         "Film3": {
#             "name": "The Man Called Flinstone (Людина, яку звуть Флінстоун) ",
#             "image": "images\\film3.png",
#             "description": "A comedy cartoon, a parody of the 1966 James Bond movies, which remains just as relevant "
#                            "today. Simple vocabulary, excellent diction, cool plot - all important components in place."
#         },
#         "Film4": {
#             "name": "Finding Nemo (У пошуках Немо)",
#             "image": "images\\film4.png",
#             "description": "A bright cartoon about fish life, which is loved by viewers of all ages. And the cartoon "
#                            "won an Oscar in 2004."
#         }
#     },
#     "A2": {
#         "Film1": {
#             "name": "The Holiday (Відпочинок за обміном).",
#             "image": "images\\film1.png",
#             "description": "Two women troubled with guy-problems swap homes in each other's countries, where they each "
#                            "meet a local guy and fall in love."
#         },
#         "Film2": {
#             "name": "My Big Fat Greek Wedding (Моє велике грецьке весілля) ",
#             "image": "images\\Theholiday.png",
#             "description": "My Big Fat Greek Wedding tells the story of Toula Portokalos. She's 30 years old and still "
#                            "not married, which means as a nice Greek girl she's a failure."
#         },
#         "Film3": {
#             "name": "The Lion King (Король Лев) ",
#             "image": "images\\thelionking.png",
#             "description": "Disney’s film journeys to the African savanna where a future king is born. Simba idolizes "
#                            "his father, King Mufasa, and takes to heart his own royal destiny. "
#         },
#         "Film4": {
#             "name": "The Wizard of Oz (Чарівник країни Оз)",
#             "image": "images\\film1.png",
#             "description": "Young Dorothy Gale and her dog are swept away by a tornado from their Kansas farm to the "
#                            "magical Land of Oz, and embark on a quest with three new friends to see the Wizard, who can "
#                            "return her to her home and fulfill the others' wishes."
#         }
#     },
#     "B1": {
#         "Film1": {
#             "name": "filmB1",
#             "description": "filmB1"
#         },
#         "Film2": {
#             "name": "2filmB1",
#             "description": "2filmB1"
#         }
#     },
#     "B2": {
#         "Film1": {
#             "name": "filmB2",
#             "description": "filmB2"
#         },
#         "Film2": {
#             "name": "2filmB2",
#             "description": "2filmB2"
#         }
#     },
#     "C1": {
#         "Film1": {
#             "name": "filmC1",
#             "description": "filmC2"
#         },
#         "Film2": {
#             "name": "2filmC1",
#             "description": "2filmC1"
#         }
#     }
# }
# books =  {
#     "A1": {
#         "Book1": {
#             "name": "Eleanor Jupp – Ski Race",
#             "image": "images\ski-jump.jpg",
#             "description": "About lovers of skiing Rebecca and Sue, who decided to take part in the competition."
#         }
#     },
#     "A2": {
#         "Book1": {
#             "name": "Eleanor Jupp – Ski Race",
#             "image": "images\ski-jump.jpg",
#             "description": "About lovers of skiing Rebecca and Sue, who decided to take part in the competition."
#         }
#     },
#     "B1": {
#         "Book1": {
#             "name": "Book1 level B1",
#             "description": "description book1"
#         },
#         "Book2": {
#             "name": "book2 level B1",
#             "description": "description book2"
#         }
#     },
#     "B2": {
#         "Book1": {
#             "name": "book1 levev B2",
#             "description": "decsription book1 b2"
#         },
#         "Book2": {
#             "name": "book2 levev B2",
#             "description": "decsription book2 b2"
#         }
#     },
#     "C1": {
#         "Book1": {
#             "name": "book1 levev C1",
#             "description": "decsription book1 C1"
#         },
#         "Book2": {
#             "name": "book2 levev C1",
#             "description": "decsription book2 C1"
#         }
#     },
# }
# with open("films.json", "w") as write_file:
#     json.dump(films, write_file, indent=3)
# with open("books.json", "w") as write_file:
#     json.dump(books, write_file, indent=3)
