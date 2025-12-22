from __future__ import annotations
from casino_lab4.settings import settings
from casino_lab4.domain.player import Player
import random as rnd

def how_many_pulls(player: Player) -> int:
    return rnd.randint(1, int(player.balance / settings.slot_spin_cost))
