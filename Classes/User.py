from Classes.Level import Level


class User:
    def __init__(self, id):
        self.__id = id
        self.__page = None
        self.__score = 0
        self.__level = Level()
        self.__number = 0

    @property
    def id(self):
        return self.__id

    @property
    def page(self):
        return self.__page

    @page.setter
    def page(self, value):
        self.__number = 0
        self.__page = value

    @property
    def score(self):
        return self.__score

    def add_score(self, value):
        if not isinstance(value, int):
            raise TypeError('value should have type "int"')
        if value <= 0:
            raise ValueError('value should be more 0')
        self.__score += value

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise TypeError('value should have type "int"')
        self.__score = value

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, value):
        if not isinstance(value, int):
            raise TypeError('value should have type "int"')
        self.__number = value

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, value):
        if not isinstance(value, str):
            raise TypeError('value should have type "str"')
        self.__level = Level(value)
