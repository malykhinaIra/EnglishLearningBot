from Interfaces.IPage import IPage


class User:
    def __init__(self, id):
        self.__id = id
        self.__page = None
        self.__score = 0
        self.__level = 'A1'

    @property
    def id(self):
        return self.__id

    @property
    def page(self):
        return self.__page

    @page.setter
    def page(self, value):
        if not isinstance(value, IPage):
            raise TypeError('value should have abstract class "IPage"')
        if self.__page:
            self.__page.exit()
        self.__page = value

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise TypeError('value should have abstract class "int"')
        self.__score = value

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, value):
        if not isinstance(value, str):
            raise TypeError('value should have type "str"')
        self.__level = value

    def close_page(self):
        self.__page.exit()
        self.__page = None
