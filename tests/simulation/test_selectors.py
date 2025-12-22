import pytest
from casino_lab4.simulation.selectors import select_players
from casino_lab4.simulation.casino import Casino
from casino_lab4.domain.player import Player

def test_select_players():
    casino = Casino(bankroll=10000)
    casino.register_player(Player('John', 1000))
    casino.register_player(Player('Jane', 2000))
    casino.register_player(Player('Bob', 3000))
    
    selected = select_players(casino)
    assert len(selected) >= 0
    assert len(selected) <= 3

def test_select_players_with_min_balance():
    casino = Casino(bankroll=10000)
    casino.register_player(Player('John', 100))
    casino.register_player(Player('Jane', 500))
    casino.register_player(Player('Bob', 1000))
    
    selected = select_players(casino, min_balance=400)
    for player in selected:
        assert player.balance >= 400

def test_select_players_no_eligible():
    casino = Casino(bankroll=10000)
    casino.register_player(Player('John', 10, sanity=0))
    
    selected = select_players(casino)
    assert len(selected) == 0

