from typing import Callable
from threading import Thread, currentThread
from telebot import *


class Timer:
    def __init__(self, bot, user_id):
        self.__bot = bot
        self.__user_id = user_id
        self.__timer_thread = None
        self.__stop_action = list()
        self.__end_action = list()

    @property
    def is_started(self):
        return True if self.__timer_thread else False

    def add_stop_action(self, value):
        if not isinstance(value, Callable):
            raise TypeError('value should be callable')
        self.__stop_action.append(value)

    def remove_stop_action(self, value):
        if not isinstance(value, Callable):
            raise TypeError('value should be callable')
        if not (value in self.__stop_action):
            raise ValueError('value is not in stop_action')
        self.__stop_action.remove(value)

    def add_end_action(self, value):
        if not isinstance(value, Callable):
            raise TypeError('value should be callable')
        self.__end_action.append(value)

    def remove_end_action(self, value):
        if not isinstance(value, Callable):
            raise TypeError('value should be callable')
        if not (value in self.__end_action):
            raise ValueError('value is not in stop_action')
        self.__end_action.remove(value)

    def start(self, minutes):
        if not isinstance(minutes, float):
            raise TypeError('time should have type "float"')
        if minutes < 1.:
            raise ValueError('time should be not less 1')
        self.stop()
        self.__timer_thread = Thread(target=self.__timer, args=(minutes,))
        self.__timer_thread.start()

    def __timer(self, minutes):
        minutes -= 0.5
        time_message = self.__bot.send_message(self.__user_id, \
                                               f'лишил{"a" if int(minutes * 2) == 3 else "o"}сь {minutes} хв')
        time.sleep(30)
        if not self.__timer_thread == currentThread():
            self.__bot.delete_message(self.__user_id, time_message.message_id)
            return
        for half_of_minute in range(int(minutes * 2) - 1, 0, -1):
            self.__bot.edit_message_text( \
                f'лишил{"a" if half_of_minute == 2 else "o"}сь {float(half_of_minute) / 2} хв', \
                self.__user_id, time_message.message_id)
            time.sleep(30)
            if not self.__timer_thread == currentThread():
                self.__bot.delete_message(self.__user_id, time_message.message_id)
                return
        self.__bot.edit_message_text('лишилось менше 30 секунд', self.__user_id, time_message.message_id)
        time.sleep(30)
        if not self.__timer_thread == currentThread():
            self.__bot.delete_message(self.__user_id, time_message.message_id)
            return
        self.__bot.delete_message(self.__user_id, time_message.message_id)
        for element in self.__end_action:
            element()

    def stop(self):
        if self.__timer_thread:
            self.__timer_thread = None
            for element in self.__stop_action:
                element()
