from abc import ABC, abstractmethod
from dataclasses import dataclass

class Entity(ABC):
    x_pos : int
    y_pos : int

    @abstractmethod
    def move(self, command) -> None:
        pass
