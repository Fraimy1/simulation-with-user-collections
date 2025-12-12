class Chip:
    def __init__(self, value: float) -> None:
        self.value = value

    def __add__(self, other):
        if isinstance(other, Chip):
            return Chip(self.value + other.value)
        if isinstance(other, int):
            return Chip(self.value + other)
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)
    
    def __repr__(self):
        return f"Chip({self.value})"