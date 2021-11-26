data = {"lecture1": ["Теоретичний матеріал лекції 1", "image1", "audio1"],
        "lecture2": ["Теоретичний матеріал лекції 2", "image2", "audio2"]}


class Lectures:
    def __init__(self, lecture=None):
        self.lecture = data[lecture][0]
        self.image = data[lecture][1]
        self.audio = data[lecture][2]
        self.test = "test"

    def __str__(self):
        return f'{self.lecture}\n{self.image}\n{self.audio}\n{self.test}'