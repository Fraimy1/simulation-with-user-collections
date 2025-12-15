from __future__ import annotations
from casino_lab4.domain.player import Player
from loguru import logger
from typing import Self
import random as rnd
from casino_lab4.utils.misc import ensure_within_100

class Goose:
    def __init__(self, name: str, honk_volume: float) -> None:
        self.name = name
        self.honk_volume = honk_volume
    
    def __add__(self, other: Self) -> Self:
        if type(other) is not type(self):
            return NotImplemented
        
        if len(self.name) + len(other.name) < 50:
            name = f"{self.name} + {other.name}"
        else:
            name = f"{self.name[:50]} + ..."
        
        cls = type(self)

        return cls(name, self.honk_volume + other.honk_volume)

    def __repr__(self) -> str:
        return f"Goose(name={self.name}, honk_volume={self.honk_volume})"

class WarGoose(Goose):
    def __init__(self, name: str, honk_volume: float, damage: float) -> None:
        super().__init__(name, honk_volume)
        self.damage = damage

    def attack(self, player: Player) -> float:
        logger.info(f"WarGoose {self.name} is attacking player {player.name} with damage {self.damage}")
        player.balance -= self.damage
        return self.damage

    def __add__(self, other: WarGoose) -> WarGoose:
        if not isinstance(other, WarGoose):
            return NotImplemented
        
        if len(self.name) + len(other.name) < 50:
            name = f"{self.name} + {other.name}"
        else:
            name = f"{self.name[:50]} + ..."
        
        return WarGoose(name, self.honk_volume + other.honk_volume, self.damage + other.damage)

    def __repr__(self) -> str:
        return f"WarGoose(name={self.name}, honk_volume={self.honk_volume}, damage={self.damage})"
    
    def attack(self) -> float:
        return self.damage * rnd.uniform(0.5, 1.5)

class HonkGoose(Goose):
    def scream(self) -> float:
        logger.info(f"HonkGoose {self.name} screamed with volume {self.honk_volume}")
        return ensure_within_100(self.honk_volume * rnd.uniform(0.5, 1.5))

    def __repr__(self) -> str:
        return f"HonkGoose(name={self.name}, honk_volume={self.honk_volume})"