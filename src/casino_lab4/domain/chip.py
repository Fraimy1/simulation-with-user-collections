from __future__ import annotations

class Chip:
    def __init__(self, value: int) -> None:
        self.value = value

    def __add__(self, other: Chip | int) -> Chip:
        if isinstance(other, Chip):
            return Chip(self.value + other.value)
        
        if isinstance(other, int):
            return Chip(self.value + other)
        
        return NotImplemented

    def __radd__(self, other: Chip | int) -> Chip:
        return self.__add__(other)
    
    def __repr__(self) -> str:
        return f"Chip({self.value})"