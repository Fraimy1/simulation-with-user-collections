from __future__ import annotations
from casino_lab4.domain.chip import Chip
class Player:
    def __init__(self, name:str, balance:float) -> None:
        self.name: str = name
        self.balance: float = balance
        self.sanity: float = 100
        self.chips: list[Chip] = []
    
    def __repr__(self) -> str:
        return f"Player(name={self.name}, balance={self.balance}, sanity={self.sanity}, chips={self.chips})"