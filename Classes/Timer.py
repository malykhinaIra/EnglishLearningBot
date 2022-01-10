from threading import Thread, currentThread
from time import sleep
from typing import Callable
from telebot import TeleBot


class Timer:
    def __init__(self, bot: TeleBot, user_id: int):
        if not isinstance(user_id, int):
            raise TypeError('user_id should have type "int"')
        if not isinstance(bot, TeleBot):
            raise TypeError('bot should have type "TeleBot"')
        self.__bot = bot
        self.__user_id = user_id
        self.__timer_thread = None
        self.__stop_action = list()
        self.__end_action = list()
        self.__update_action = list()

    @property
    def is_started(self) -> bool:
        return True if self.__timer_thread else False

    def add_stop_action(self, value: Callable):
        if not isinstance(value, Callable):
            raise TypeError('value should be callable')
        self.__stop_action.append(value)

    def remove_stop_action(self, value: Callable):
        if not isinstance(value, Callable):
            raise TypeError('value should be callable')
        if not (value in self.__stop_action):
            raise ValueError('value is not in stop_action')
        self.__stop_action.remove(value)

    def add_end_action(self, value: Callable):
        if not isinstance(value, Callable):
            raise TypeError('value should be callable')
        self.__end_action.append(value)

    def remove_end_action(self, value: Callable):
        if not isinstance(value, Callable):
            raise TypeError('value should be callable')
        if not (value in self.__end_action):
            raise ValueError('value is not in end_action')
        self.__end_action.remove(value)

    def add_update_action(self, value: Callable):
        if not isinstance(value, Callable):
            raise TypeError('value should be callable')
        self.__update_action.append(value)

    def remove_update_action(self, value: Callable):
        if not isinstance(value, Callable):
            raise TypeError('value should be callable')
        if not (value in self.__update_action):
            raise ValueError('value is not in update_action')
        self.__update_action.remove(value)

    def start(self, minutes: int or float):
        if not isinstance(minutes, int) and not isinstance(minutes, float):
            raise TypeError('time should have type "int" or "float"')
        if minutes < 1.:
            raise ValueError('time should be not less 1')
        self.stop()
        self.__timer_thread = Thread(target=self.__timer, args=(minutes,))
        self.__timer_thread.start()

    def __update(self, minutes_left: int or float):
        for element in self.__update_action:
            element(minutes_left)

    def __timer(self, minutes: int or float):
        minutes -= 0.5
        self.__update(minutes)
        sleep(30)
        if not self.__timer_thread == currentThread():
            return
        for half_of_minute in range(int(minutes * 2) - 1, 0, -1):
            self.__update(float(half_of_minute) / 2.)
            sleep(30)
            if not self.__timer_thread == currentThread():
                return
        self.__update(0)
        sleep(30)
        if not self.__timer_thread == currentThread():
            return
        self.__timer_thread = None
        for element in self.__end_action:
            element()

    def stop(self):
        if self.__timer_thread:
            self.__timer_thread = None
            for element in self.__stop_action:
                element()
