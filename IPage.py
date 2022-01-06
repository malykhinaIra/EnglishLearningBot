from abc import ABC, abstractmethod


class IPage(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def exit(self):
        pass

    @abstractmethod
    def keyboard(self):
        pass
