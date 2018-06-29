from abc import ABC, abstractmethod


class GameState(ABC):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abstractmethod
    def process_input(self):
        pass

    @abstractmethod
    def process_updates(self, delta_time):
        pass

    @abstractmethod
    def process_drawing(self, display):
        pass

    @abstractmethod
    def on_enter(self):
        pass

    @abstractmethod
    def on_exit(self):
        pass
