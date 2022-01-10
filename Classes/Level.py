from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class Level:
    __levels = ["A1", "A2", "B1", "B2", "C1", "None"]

    def __init__(self, level: str = 'None'):
        if not isinstance(level, str):
            raise TypeError('level should have type "str"')
        if not (level in Level.__levels):
            raise ValueError('value of level should be "A1","A2","B1","B2","C1","C2","None"')
        self.__level = level
        if level == "None":
            self.__keyboard = InlineKeyboardMarkup()
            self.__keyboard.add(InlineKeyboardButton(text="Тест на рівень англійської",
                                                     url="https://englex.ru/your-level/"))
            self.__keyboard.add(InlineKeyboardButton(text='Я знаю свій рівень:', callback_data='answer'))
        else:
            self.__keyboard = InlineKeyboardMarkup()
            self.__keyboard.add(InlineKeyboardButton(text='Фільм', callback_data='film'))
            self.__keyboard.add(InlineKeyboardButton(text='Книга', callback_data='book'))
            self.__keyboard.add(InlineKeyboardButton(text="Підвищити рівень",
                                                     callback_data='up'))
            self.__keyboard.add(InlineKeyboardButton(text='Знизити рівень', callback_data='down'))

    @property
    def level(self):
        return self.__level

    @property
    def keyboard(self):
        return self.__keyboard

    def up_level(self):
        if self.__level == 'A1':
            self.__level = 'A2'
        elif self.__level == 'A2':
            self.__level = 'B1'
        elif self.__level == 'B1':
            self.__level = 'B2'
        elif self.__level == 'B2':
            self.__level = 'C1'
        elif self.__level == 'C1':
            self.__level = 'C2'

    def down_level(self):
        if self.__level == 'C2':
            self.__level = 'C1'
        elif self.__level == 'C1':
            self.__level = 'B2'
        elif self.__level == 'B2':
            self.__level = 'B1'
        elif self.__level == 'B1':
            self.__level = 'A2'
        elif self.__level == 'A2':
            self.__level = 'A1'
