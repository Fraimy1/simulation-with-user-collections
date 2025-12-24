from casino_lab4.simulation.events import (
    event_roulette,
    event_slots,
    event_honk_scream,
    event_wargoose_attack,
    event_sanity_break,
    event_russian_roulette,
    event_bankrupt,
    pick_event,
    available_events,
    call_mandatory_events,
    RANDOM_EVENTS,
)
from casino_lab4.simulation.casino import Casino
from casino_lab4.domain.player import Player
from casino_lab4.domain.goose import WarGoose, HonkGoose


def test_event_roulette():
    casino = Casino(bankroll=10000)
    player = Player("John", 1000)
    casino.register_player(player)

    event_roulette(casino)

    assert casino.bankroll != 10000 or player.balance != 1000


def test_event_roulette_no_players():
    casino = Casino(bankroll=10000)
    event_roulette(casino)
    assert casino.bankroll == 10000


def test_event_roulette_bankrupt_casino():
    casino = Casino(bankroll=10000)
    casino.is_bankrupt = True
    player = Player("John", 1000)
    casino.register_player(player)

    event_roulette(casino)
    assert player.balance == 1000


def test_event_slots():
    casino = Casino(bankroll=10000)
    player = Player("John", 1000)
    casino.register_player(player)

    initial_balance = player.balance
    initial_bankroll = casino.bankroll

    event_slots(casino)

    assert player.balance != initial_balance or casino.bankroll != initial_bankroll


def test_event_slots_no_players():
    casino = Casino(bankroll=10000)
    event_slots(casino)
    assert casino.bankroll == 10000


def test_event_honk_scream():
    casino = Casino(bankroll=10000)
    player = Player("John", 1000, sanity=100)
    goose = HonkGoose("Honker", 10, balance=0)
    casino.register_player(player)
    casino.register_goose(goose)

    initial_sanity = player.sanity
    initial_goose_balance = goose.balance
    event_honk_scream(casino)

    assert player.sanity <= initial_sanity or goose.balance >= initial_goose_balance


def test_event_honk_scream_no_geese():
    casino = Casino(bankroll=10000)
    player = Player("John", 1000)
    casino.register_player(player)

    event_honk_scream(casino)
    assert player.sanity == 100


def test_event_wargoose_attack():
    casino = Casino(bankroll=10000)
    player = Player("John", 1000)
    goose = WarGoose("Warrior", 10, 20, balance=0)
    casino.register_player(player)
    casino.register_goose(goose)

    initial_balance = player.balance
    initial_goose_balance = goose.balance
    event_wargoose_attack(casino)

    assert player.balance <= initial_balance or goose.balance >= initial_goose_balance


def test_event_wargoose_attack_no_geese():
    casino = Casino(bankroll=10000)
    player = Player("John", 1000)
    casino.register_player(player)

    event_wargoose_attack(casino)
    assert player.balance == 1000


def test_event_sanity_break():
    casino = Casino(bankroll=10000)
    player = Player("John", 1000, sanity=0)
    casino.register_player(player)

    event_sanity_break(casino)


def test_event_russian_roulette():
    casino = Casino(bankroll=10000)
    player1 = Player("John", 0)
    player2 = Player("Jane", 0)
    casino.register_player(player1)
    casino.register_player(player2)

    event_russian_roulette(casino)


def test_event_russian_roulette_not_enough_broke():
    casino = Casino(bankroll=10000)
    player = Player("John", 0)
    casino.register_player(player)

    event_russian_roulette(casino)
    assert player.alive


def test_event_bankrupt():
    casino = Casino(bankroll=10000)
    event_bankrupt(casino)
    assert casino.is_bankrupt


def test_pick_event():
    casino = Casino(bankroll=10000)
    event = pick_event(casino)
    assert event in RANDOM_EVENTS


def test_pick_event_weighted():
    casino = Casino(bankroll=10000)
    event = pick_event(casino, weighted=True)
    assert event in RANDOM_EVENTS


def test_pick_event_unweighted():
    casino = Casino(bankroll=10000)
    event = pick_event(casino, weighted=False)
    assert event in RANDOM_EVENTS


def test_available_events():
    casino = Casino(bankroll=10000)
    events = available_events(casino)
    assert len(events) > 0


def test_available_events_bankrupt():
    casino = Casino(bankroll=10000)
    casino.is_bankrupt = True
    events = available_events(casino)
    assert len(events) == 0


def test_call_mandatory_events():
    casino = Casino(bankroll=10000)
    player = Player("John", 1000)
    casino.register_player(player)

    call_mandatory_events(casino)


def test_call_mandatory_events_bankrupt():
    casino = Casino(bankroll=10000)
    casino.is_bankrupt = True
    call_mandatory_events(casino)
    assert casino.is_bankrupt


def test_call_mandatory_events_no_bankroll():
    casino = Casino(bankroll=0)
    call_mandatory_events(casino)
    assert casino.is_bankrupt


def test_event_roulette_casino_cant_pay():
    casino = Casino(bankroll=10)
    player = Player("John", 1000)
    casino.register_player(player)

    for _ in range(100):
        event_roulette(casino)
        if casino.is_bankrupt:
            break


def test_event_slots_casino_cant_pay():
    casino = Casino(bankroll=10)
    player = Player("John", 1000)
    casino.register_player(player)

    for _ in range(100):
        event_slots(casino)
        if casino.is_bankrupt:
            break


def test_event_slots_player_broke():
    casino = Casino(bankroll=10000)
    player = Player("John", 0)
    casino.register_player(player)

    event_slots(casino)
    assert player.balance == 0


def test_event_russian_roulette_multiple_rounds():
    casino = Casino(bankroll=10000)
    for i in range(10):
        casino.register_player(Player(f"Player{i}", 0))

    event_russian_roulette(casino)


def test_event_sanity_break_multiple_players():
    casino = Casino(bankroll=10000)
    casino.register_player(Player("John", 1000, sanity=0))
    casino.register_player(Player("Jane", 2000, sanity=10))
    casino.register_player(Player("Bob", 3000, sanity=0))

    event_sanity_break(casino)


def test_event_wargoose_attack_kill_player():
    casino = Casino(bankroll=10000)
    player = Player("John", 10)
    goose = WarGoose("Killer", 10, 100, balance=0)
    casino.register_player(player)
    casino.register_goose(goose)

    for _ in range(50):
        if not player.alive:
            break
        event_wargoose_attack(casino)


def test_event_honk_scream_multiple_victims():
    casino = Casino(bankroll=10000)
    for i in range(5):
        casino.register_player(Player(f"Player{i}", 1000, sanity=100))
    goose = HonkGoose("Screamer", 50, balance=0)
    casino.register_goose(goose)

    event_honk_scream(casino)
