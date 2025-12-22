import pytest
from casino_lab4.simulation.setup import create_default_casino
from casino_lab4.domain.goose import WarGoose, HonkGoose

def test_create_default_casino():
    casino = create_default_casino()

    assert casino.bankroll == 100000.0
    assert len(casino.players) == 8
    assert len(casino.geese) == 5

    player_names = [p.name for p in casino.players]
    assert "Jane" in player_names
    assert "Dante" in player_names
    assert "Vergil" in player_names
    assert "V" in player_names
    assert "Charlie" in player_names
    assert "Samir" in player_names
    assert "John" in player_names
    assert "Daniel" in player_names

    for player in casino.players:
        assert player.balance > 0
        assert player.sanity == 100

    war_geese = [g for g in casino.geese if isinstance(g, WarGoose)]
    honk_geese = [g for g in casino.geese if isinstance(g, HonkGoose)]

    assert len(war_geese) == 3
    assert len(honk_geese) == 2
