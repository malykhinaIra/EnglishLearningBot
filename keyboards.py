from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


class MainKeyboard:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*[KeyboardButton(name) for name in ['Тести', 'Лекції']])
    keyboard.add(*[KeyboardButton(name) for name in ['Ігри', 'Що подивитись/почитати?']])


class LevelKeyboard:
    keyboard = InlineKeyboardMarkup()
    url_button = InlineKeyboardButton(text="Тест на рівень англійської",
                                      url="https://englex.ru/your-level/")
    key_level = InlineKeyboardButton(text='Я знаю свій рівень:', callback_data='answer')
    keyboard.add(url_button)
    keyboard.add(key_level)


class TestKeyboard:
    keyboard = InlineKeyboardMarkup()
    key_test = InlineKeyboardButton(text='Розпочати', callback_data='tests')
    keyboard.add(key_test)


class RecommendKeyboard:
    keyboard = InlineKeyboardMarkup()
    key_film = InlineKeyboardButton(text='Фільм', callback_data='film')
    keyboard.add(key_film)
    key_book = InlineKeyboardButton(text='Книга', callback_data='book')
    keyboard.add(key_book)
    keyboard.add(InlineKeyboardButton(text="Підвищити рівень", callback_data='up'))
    keyboard.add(InlineKeyboardButton(text='Знизити рівень', callback_data='down'))


class GameKeyboard:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Мішанина", callback_data="cipher"))
    keyboard.add(InlineKeyboardButton(text="Перекладач", callback_data="translate"))
    keyboard.add(InlineKeyboardButton(text="Загадки", callback_data="riddles"))

