from abc import ABC, abstractmethod


class GenericKafkaActor(ABC):

    @abstractmethod
    def process(self, message):
        """Метод для обработки данных."""
        raise NotImplementedError(
            "process() method is not implemented")

    @abstractmethod
    def output(self):
        """Метод для вывода результатов."""
        raise NotImplementedError(
            "output() method is not implemented")