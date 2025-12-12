class Chip:
    def __init__(self, value: float) -> None:
        self.value = value

    def __add__(self, chip_2: "Chip"):
        return self.value + chip_2.value

