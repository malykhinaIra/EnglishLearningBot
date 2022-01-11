from keyboards import LevelKeyboard, RecommendKeyboard


class Level:
    """Class for getting the level of english"""

    __levels = ["A1", "A2", "B1", "B2", "C1", "None"]

    def __init__(self, level: str = 'None'):
        self.level = level
        if level == "None":
            self.keyboard = LevelKeyboard.keyboard
        else:
            self.keyboard = RecommendKeyboard.keyboard

    @property
    def level(self):
        """Get user’s level"""
        return self._level

    @level.setter
    def level(self, level):
        if not isinstance(level, str):
            raise TypeError('level should have type "str"')
        if not (level in Level.__levels):
            raise ValueError('value of level should be "A1","A2","B1","B2","C1","None"')
        self._level = level

    @property
    def keyboard(self):
        """Get keybord with recommend menu"""
        return self._keyboard

    def up_level(self):
        """Function for up your level of english"""
        if self.level == 'A1':
            self.level = 'A2'
        elif self.level == 'A2':
            self.level = 'B1'
        elif self.level == 'B1':
            self.level = 'B2'
        elif self.level == 'B2':
            self.level = 'C1'

    def down_level(self):
        """Function for down your level of english"""
        if self.level == 'C1':
            self.level = 'B2'
        elif self.level == 'B2':
            self.level = 'B1'
        elif self.level == 'B1':
            self.level = 'A2'
        elif self.level == 'A2':
            self.level = 'A1'

    @level.setter
    def level(self, value):
        self._level = value

    @keyboard.setter
    def keyboard(self, value):
        self._keyboard = value

    @keyboard.setter
    def keyboard(self, value):
        self._keyboard = value

    @keyboard.setter
    def keyboard(self, value):
        self._keyboard = value
