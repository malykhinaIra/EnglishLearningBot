from abc import ABC, abstractmethod


class ITest(ABC):
    @abstractmethod
    def passing_test(self, answer):
        pass
