import pytest
from casino_lab4.domain.goose import Goose, WarGoose, HonkGoose
from casino_lab4.domain.player import Player

def test_goose():
    goose_1 = Goose('John', 2)
    goose_2 = Goose('Dan', 3)

    assert goose_1.name == 'John'
    assert goose_1.honk_volume == 2
    assert goose_1.balance == 0.0

    assert repr(goose_1) == "Goose(name=John, honk_volume=2, balance=0.0)"

    new_goose = goose_1 + goose_2
    assert new_goose.name == 'John + Dan'
    assert new_goose.honk_volume == 5
    assert new_goose.balance == 0.0

    with pytest.raises(TypeError):
        goose_1 + 7

def test_goose_with_balance():
    goose = Goose('Rich', 5, balance=100.0)
    assert goose.balance == 100.0

def test_goose_long_name():
    goose_1 = Goose('A' * 30, 2)
    goose_2 = Goose('B' * 30, 3)
    new_goose = goose_1 + goose_2
    assert len(new_goose.name) <= 55

def test_war_goose():
    war_goose_1 = WarGoose('John', 2, 10)
    war_goose_2 = WarGoose('Dan', 3, 15)

    new_war_goose = war_goose_1 + war_goose_2
    assert new_war_goose.name == 'John + Dan'
    assert new_war_goose.honk_volume == 5
    assert new_war_goose.damage == 25
    assert repr(new_war_goose) == "WarGoose(name=John + Dan, honk_volume=5, damage=25, balance=0.0)"

    with pytest.raises(TypeError):
        war_goose_1 + 7

def test_war_goose_attack():
    war_goose = WarGoose('Fighter', 5, 20)
    damage = war_goose.attack()
    assert 10 <= damage <= 30

def test_war_goose_long_name():
    war_goose_1 = WarGoose('A' * 30, 2, 10)
    war_goose_2 = WarGoose('B' * 30, 3, 15)
    new_war_goose = war_goose_1 + war_goose_2
    assert len(new_war_goose.name) <= 55

def test_honk_goose():
    honk_goose_1 = HonkGoose('John', 2)
    honk_goose_2 = HonkGoose('Dan', 3)

    scream_value = honk_goose_1.scream()
    assert 0 <= scream_value <= 100
    assert repr(honk_goose_1) == "HonkGoose(name=John, honk_volume=2, balance=0.0)"

    g = honk_goose_1 + honk_goose_2
    assert g.name == 'John + Dan'
    assert g.honk_volume == 5
    assert repr(g) == "HonkGoose(name=John + Dan, honk_volume=5, balance=0.0)"
