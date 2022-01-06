from telebot import TeleBot
from Classes.User import User


class BotWithPages(TeleBot):
    def __init__(self, token):
        super().__init__(token)
        self.__users = dict()

    def get_user(self, user_id: int):
        if not isinstance(user_id, int):
            raise TypeError('user_id should have type "int"')
        if not (user_id in self.__users):
            return None
        return self.__users[user_id]

    def set_user(self, value):
        if not isinstance(value, User) and not isinstance(value, int):
            raise TypeError('value should be class "User" or type "int"')
        if isinstance(value, int):
            value = User(value)
        if value.id in self.__users:
            self.__users[value.id].page.exit()
        self.__users[value.id] = value
