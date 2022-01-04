from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


class MainKeyboard:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*[KeyboardButton(name) for name in ['Тести', 'Лекції']])
    keyboard.add(*[KeyboardButton(name) for name in ['Ігри', 'Що подивитись/почитати?']])


class GameKeyboard:
    key_word = InlineKeyboardButton(text='Слова', callback_data='words')
    key_cipher = InlineKeyboardButton(text='Розшифруй слово', callback_data='cipher')
    key_translate = InlineKeyboardButton(text='Перекладач', callback_data='translate')
    key_riddles = InlineKeyboardButton(text='Загадки', callback_data='riddles')
    keyboard = InlineKeyboardMarkup()
    keyboard.add(key_word)
    keyboard.add(key_cipher)
    keyboard.add(key_translate)
    keyboard.add(key_riddles)


class LectionsKeyboard:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Дієслово (Verb)', callback_data='1'))
    keyboard.add(InlineKeyboardButton(text='Герундій (Gerund)', callback_data='2'))
    keyboard.add(InlineKeyboardButton(text='Інфінітив (Infinitive)', callback_data='3'))
    keyboard.add(InlineKeyboardButton(text='Неправильні дієслова (Irregular Verbs)', callback_data='4'))
    keyboard.add(InlineKeyboardButton(text='Фразові дієслова (Phrasal Verbs)', callback_data='5'))
    keyboard.add(*[InlineKeyboardButton(name, callback_data=name) for name in ['◀', '▶']])


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
