from casino_lab4.simulation.randomization import how_many_pulls
from casino_lab4.domain.player import Player
from casino_lab4.settings import settings


def test_how_many_pulls():
    player = Player("John", 1000)
    pulls = how_many_pulls(player)
    max_pulls = int(player.balance / settings.slot_spin_cost)
    assert pulls >= 1
    assert pulls <= max_pulls
