from __future__ import annotations

class Chip:
    def __init__(self, value: int, color: str = "default", number: int = 1) -> None:
        self.color: str = color
        self.value: int = value
        self.number: int = number

    def __add__(self, other: Chip | int) -> Chip:
        if isinstance(other, Chip):
            return Chip(self.value + other.value, self.color, self.number + other.number)
        
        if isinstance(other, int):
            return Chip(self.value + other, self.color, self.number)
        
        return NotImplemented

    def __radd__(self, other: Chip | int) -> Chip:
        return self.__add__(other)
    
    def __repr__(self) -> str:
        return f"Chip({self.value})"