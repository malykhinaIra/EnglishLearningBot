from abc import ABC, abstractmethod


class IRecomendations(ABC):
    @abstractmethod
    def image(self):
        pass

    @abstractmethod
    def description(self):
        pass
