import pytest
from casino_lab4.domain.goose import Goose, WarGoose, HonkGoose
from casino_lab4.domain.player import Player

def test_goose():
    goose_1 = Goose('John', 2)
    goose_2 = Goose('Dan', 3)

    assert goose_1.name == 'John'
    assert goose_1.honk_volume == 2

    # assert repr(goose_1) == "Goose(name=John, honk_volume=2)"

    new_goose = goose_1 + goose_2
    assert new_goose.name == 'John + Dan'
    assert new_goose.honk_volume == 5
    
    with pytest.raises(TypeError):
        goose_1 + 7

def test_war_goose():
    war_goose_1 = WarGoose('John', 2, 10)
    war_goose_2 = WarGoose('Dan', 3, 15)

    new_war_goose = war_goose_1 + war_goose_2
    assert new_war_goose.name == 'John + Dan'
    assert new_war_goose.honk_volume == 5
    assert new_war_goose.damage == 25
    # assert repr(new_war_goose) == "WarGoose(name=John + Dan, honk_volume=5, damage=25)"

    with pytest.raises(TypeError):
        war_goose_1 + 7

def test_honk_goose():
    honk_goose_1 = HonkGoose('John', 2)
    honk_goose_2 = HonkGoose('Dan', 3)

    assert honk_goose_1.scream() == 2
    # assert repr(honk_goose_1) == "HonkGoose(name=John, honk_volume=2)"

    g = honk_goose_1 + honk_goose_2
    assert g.name == 'John + Dan'
    assert g.honk_volume == 5
    # assert repr(g) == "HonkGoose(name=John + Dan, honk_volume=5)"