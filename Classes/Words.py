import json
import os
from typing import List


class Words(json.JSONEncoder):
    def default(self, obj):
        return json.JSONEncoder.default(self, obj)

    @classmethod
    def read_words(cls, file_name: str = 'jsonFiles/words.json') -> List[List[str]]:
        if not os.path.isfile(file_name):
            raise FileExistsError(f'file {file_name} does not exist')
        with open(file_name, 'r', encoding='utf-8') as file:
            words = json.loads(file.read())
            file.close()
            return words

    @classmethod
    def read_word(cls, name: str, file_name: str = 'jsonFiles/words.json') -> List[str]:
        if not os.path.isfile(file_name):
            raise FileExistsError(f'file {file_name} does not exist')
        with open(file_name, 'r', encoding='utf-8') as file:
            words = json.loads(file.read())
            word_translates = list()
            for element in words:
                if element[0] == name:
                    word_translates.append(element[1])
            file.close()
            return word_translates

    @classmethod
    def write_word(cls, name: str, translate: str, file_name: str = 'jsonFiles/words.json'):
        if not isinstance(name, str):
            raise TypeError('name should have type "str"')
        if not isinstance(translate, str):
            raise TypeError('translate should have type "str"')
        if not isinstance(file_name, str):
            raise TypeError('file_name should have type "str"')
        if not os.path.isfile(file_name):
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(json.dumps([[name, translate]], cls=Words))
                file.close()
        elif not (translate in cls.read_word(name, file_name)):
            with open(file_name, 'a+') as file:
                file.seek(file.truncate(file.tell() - 1))
                file.write(f',\n["{name}","{translate}"]]')
                file.close()
