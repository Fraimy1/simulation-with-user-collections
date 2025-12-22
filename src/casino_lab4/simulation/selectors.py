from __future__ import annotations
from casino_lab4.simulation.casino import Casino
import random as rnd
from casino_lab4.collections.players import PlayerCollection

def select_players(casino: Casino, min_balance: float = 0) -> PlayerCollection:
    """Selects a random subset of players that can act and have at least min_balance"""
    players = [player for player in casino.players._data if player.can_act() and player.balance >= min_balance]
    if not players:
        return PlayerCollection([])

    n_players = len(players)
    n_select = rnd.randint(1, int(n_players/2))
    picked = rnd.sample(players, n_select)
    return PlayerCollection(picked)
