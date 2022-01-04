import json
with open("jsonFiles/lectures.json", 'r', encoding="utf-8") as file:
    data = json.load(file)


class Lectures:
    def __init__(self, lecture=None):
        self.name = data[lecture]["name"]
        self.text = data[lecture]["text"]
        self.image = data[lecture]["image"]
        self.audio = None
        self.test = "test"
        self.index = int(lecture)

    def __str__(self):
        return f'\b{self.name}\b\n\n{self.text}'
