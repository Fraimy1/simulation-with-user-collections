from __future__ import annotations

import random as rnd

from casino_lab4.settings import settings
from casino_lab4.simulation.casino import Casino
from casino_lab4.domain.player import Player
from casino_lab4.domain.goose import Goose, WarGoose, HonkGoose


def create_default_casino() -> Casino:
    casino = Casino(bankroll=100000.0)

    player_names = ["Jane", "Dante", "Vergil", "V", "Charlie", "Samir", "John", "Daniel"]
    for name in player_names:
        balance = float(rnd.randint(
            settings.player_start_cash_min,
            settings.player_start_cash_max
        ))
        sanity = settings.sanity_max
        player = Player(name=name, balance=balance, sanity=sanity)
        casino.register_player(player)

    war_goose_names = ["Goose1", "Goose2", "Goose3"]
    for name in war_goose_names:
        honk_volume = rnd.uniform(5, 15)
        damage = rnd.uniform(10, 30)
        goose = WarGoose(name=name, honk_volume=honk_volume, damage=damage, balance=0.0)
        casino.register_goose(goose)

    honk_goose_names = ["Goose4", "Goose5"]
    for name in honk_goose_names:
        honk_volume = rnd.uniform(8, 20)
        goose = HonkGoose(name=name, honk_volume=honk_volume, balance=0.0)
        casino.register_goose(goose)

    return casino
