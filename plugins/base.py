from abc import ABC, abstractmethod


class BasePlugin(ABC):

    @abstractmethod
    def execute(self, config: dict) -> dict:
        pass