from abc import abstractmethod


class Game:
    # self.user_id
    # self.difficulty
    # self.is_started
    # self.time
    # reward

    def __init__(self, **kwargs):
        pass

    def start(self):
        pass

    @abstractmethod
    def rules(self):
        pass

    def change_difficulty(self):
        pass

    @classmethod
    def get_statistics(cls):
        pass

    @abstractmethod
    def set_value(self):
        pass

    @abstractmethod
    def exit(self, is_victory):
        pass


class TranslatorGame(Game):
    # time
    # reward
    def __init__(self, **kwargs):
        pass

    def rules(self):
        pass

    @classmethod
    def get_statistics(cls):
        pass

    def set_value(self):
        pass

    def exit(self, is_victory):
        pass

    def __str__(self):
        return f'яблуко'


class PuzzleGame(Game):
    # time
    # reward
    def rules(self):
        pass

    @classmethod
    def get_statistics(cls):
        pass

    def set_value(self):
        pass

    def exit(self, is_victory):
        pass

    def __str__(self):
        return f'New York is also called: "Big ...'


class MixGame(Game):
    # time
    # reward
    def rules(self):
        pass

    @classmethod
    def get_statistics(cls):
        pass

    def set_value(self):
        pass

    def exit(self, is_victory):
        pass

    def __str__(self):
        return f'paple'


class FirstLetterGame(Game):
    # time
    # reward
    def rules(self):
        pass

    @classmethod
    def get_statistics(cls):
        pass

    def set_value(self):
        pass

    def exit(self, is_victory):
        pass

    def __str__(self):
        return f'ApplE'
