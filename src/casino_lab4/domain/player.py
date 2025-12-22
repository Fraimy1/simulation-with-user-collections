from __future__ import annotations


class Player:
    def __init__(self, name: str, balance: float, sanity: int = 100) -> None:
        self.name: str = name
        self.balance: float = balance
        self.sanity: int = sanity
        self.alive: bool = True

    def __repr__(self) -> str:
        return f"Player(name={self.name}, balance={self.balance}, sanity={self.sanity}, alive={self.alive})"

    def __str__(self) -> str:
        return f"Player(name={self.name}, balance={self.balance}, sanity={self.sanity}, alive={self.alive})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return False
        return (
            self.name == other.name
            and self.balance == other.balance
            and self.sanity == other.sanity
            and self.alive == other.alive
        )

    def apply_sanity(self, sanity: int) -> None:
        self.sanity = max(min(sanity, 100), 0)

    def rest(self) -> None:
        self.sanity = 100

    def can_act(self) -> bool:
        return self.sanity > 0 and self.alive

    def die(self) -> None:
        self.alive = False
        self.sanity = 100
