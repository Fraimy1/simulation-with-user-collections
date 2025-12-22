from __future__ import annotations

import random as rnd

from casino_lab4.settings import settings
from casino_lab4.simulation.casino import Casino
from casino_lab4.simulation.event_types import Event
from casino_lab4.utils.logging import logger

from casino_lab4.domain.goose import HonkGoose, WarGoose
from casino_lab4.domain.player import Player


def _sync_balance(casino: Casino, player: Player) -> None:
    casino.balances[player.name] = float(player.balance)


def _sync_goose_balance(casino: Casino, goose) -> None:
    casino.geese_balances[goose.name] = float(goose.balance)


def _alive_players(casino: Casino) -> list[Player]:
    return [p for p in casino.players if getattr(p, "alive", True)]


def _players_with_min_balance(casino: Casino, min_balance: float) -> list[Player]:
    return [p for p in _alive_players(casino) if float(p.balance) >= float(min_balance)]


def _broke_players(casino: Casino) -> list[Player]:
    return [p for p in _alive_players(casino) if float(p.balance) <= 0.0]


def _mark_bankrupt(casino: Casino, reason: str) -> None:
    setattr(casino, "is_bankrupt", True)
    logger.info(f"Bankrupt: {reason} -> game over")


def _roulette_roll() -> str:
    return rnd.choices(
        population=settings.roulette_outcomes,
        weights=settings.roulette_weights,
        k=1,
    )[0]


def _roulette_user_choice() -> str:
    allowed = set(settings.roulette_outcomes)
    outcomes = [o for o in settings.roulette_user_choice_outcomes if o in allowed]
    weights = [
        settings.roulette_user_choice_probabilities[o]
        for o in outcomes
    ]
    return rnd.choices(outcomes, weights=weights, k=1)[0]


def event_roulette(casino: Casino) -> None:
    if getattr(casino, "is_bankrupt", False):
        return

    eligible = [p for p in _alive_players(casino) if p.can_act() and p.balance > 0]
    if not eligible:
        logger.info("Roulette: no eligible players")
        return

    players = eligible.copy()
    rnd.shuffle(players)

    for player in players:
        bet_cap = min(int(player.balance), 100)
        bet = rnd.randint(1, max(1, bet_cap))

        user_choice = _roulette_user_choice()
        roll = _roulette_roll()

        player.balance -= bet
        casino.bankroll += bet
        _sync_balance(casino, player)

        if roll != user_choice:
            logger.info(f"Roulette: {player.name} bet={bet} on {user_choice}, roll={roll} -> LOSE")
            continue

        mult = settings.roulette_payout_total.get(user_choice)
        if mult is None:
            logger.info(f"Roulette: missing payout multiplier for {user_choice}")
            continue

        total_return = bet * int(mult)

        if casino.bankroll < total_return:
            _mark_bankrupt(casino, f"roulette can't pay {player.name} total_return={total_return}, bankroll={casino.bankroll:.2f}")
            return

        player.balance += total_return
        casino.bankroll -= total_return
        _sync_balance(casino, player)

        profit = total_return - bet
        logger.info(f"Roulette: {player.name} bet={bet} on {user_choice}, roll={roll} -> WIN profit={profit}")


def _slots_spin_outcome() -> str:
    return rnd.choices(
        population=settings.slot_outcomes,
        weights=settings.slot_weights,
        k=1,
    )[0]


def _slots_pull(casino: Casino, player: Player, bet: int) -> str:
    player.balance -= bet
    casino.bankroll += bet
    _sync_balance(casino, player)

    outcome = _slots_spin_outcome()

    sanity_delta = int(settings.slot_sanity_delta.get(outcome, 0))
    player.apply_sanity(player.sanity + sanity_delta)

    mult = int(settings.slot_payout_total.get(outcome, 0))
    total_return = bet * mult

    if total_return > 0:
        if casino.bankroll < total_return:
            _mark_bankrupt(casino, f"slots can't pay {player.name} total_return={total_return}, bankroll={casino.bankroll:.2f}")
            return outcome

        player.balance += total_return
        casino.bankroll -= total_return
        _sync_balance(casino, player)

    return outcome


def event_slots(casino: Casino) -> None:
    if getattr(casino, "is_bankrupt", False):
        return

    bet = int(settings.slot_spin_cost)
    if bet <= 0:
        logger.info("Slots: invalid spin cost")
        return

    eligible = [p for p in _alive_players(casino) if p.can_act() and p.balance > 0]
    if not eligible:
        logger.info("Slots: no eligible players")
        return

    players = eligible.copy()
    rnd.shuffle(players)

    for player in players:
        max_pulls = max(1, int(player.balance // bet))
        pulls = rnd.randint(1, min(max_pulls, 10))

        wins = 0
        for _ in range(pulls):
            if getattr(casino, "is_bankrupt", False):
                return
            outcome = _slots_pull(casino, player, bet)
            if outcome != "MISS":
                wins += 1

        logger.info(f"Slots: {player.name} pulls={pulls}, wins={wins} -> balance={player.balance:.2f}, sanity={player.sanity}")


def event_honk_scream(casino: Casino) -> None:
    if getattr(casino, "is_bankrupt", False):
        return

    geese = [g for g in casino.geese if isinstance(g, HonkGoose)]
    players = _alive_players(casino)

    if not geese or not players:
        logger.info("Honk: no HonkGoose or no players")
        return

    goose = rnd.choice(geese)

    victims_n = rnd.randint(1, min(3, len(players)))
    victims = rnd.sample(players, k=victims_n)

    debuff = int(goose.scream())
    total_stolen = 0.0
    for p in victims:
        p.apply_sanity(p.sanity - debuff)

        if p.balance > 0:
            fee = min(p.balance * 0.05, 50.0)
            p.balance -= fee
            goose.balance += fee
            total_stolen += fee
            _sync_balance(casino, p)

    if total_stolen > 0:
        _sync_goose_balance(casino, goose)

    logger.info(f"Honk: {goose.name} screamed -> sanity -{debuff} to {len(victims)} player(s), stole ${total_stolen:.2f} -> goose balance={goose.balance:.2f}")


def event_wargoose_attack(casino: Casino) -> None:
    if getattr(casino, "is_bankrupt", False):
        return

    geese = [g for g in casino.geese if isinstance(g, WarGoose)]
    players = _alive_players(casino)  # All alive players can be attacked, regardless of balance

    if not geese or not players:
        logger.info("Attack: no WarGoose or no players")
        return

    goose = rnd.choice(geese)

    k = rnd.randint(settings.wargoose_attack_victims_min, settings.wargoose_attack_victims_max)
    k = max(1, min(len(players), int(k)))
    victims = rnd.sample(players, k=k)

    pct = rnd.uniform(settings.wargoose_steal_pct_min, settings.wargoose_steal_pct_max)

    total = 0.0
    for v in victims:
        if v.balance <= 0:
            continue
        stolen = float(v.balance) * float(pct)
        stolen = max(0.0, min(float(v.balance), stolen))
        v.balance -= stolen
        goose.balance += stolen  # Money goes to the goose, not casino!
        total += stolen
        _sync_balance(casino, v)

    if total > 0:
        _sync_goose_balance(casino, goose)

    logger.info(f"Attack: {goose.name} stole ~{pct:.0%} from {len(victims)} player(s), total={total:.2f} -> goose balance={goose.balance:.2f}")


def event_sanity_break(casino: Casino) -> None:
    players = _alive_players(casino)
    broken = [p for p in players if int(p.sanity) <= 0]

    if not broken:
        return

    rested = 0
    for p in broken:
        if rnd.random() < float(settings.sanity_skip_turn_chance):
            p.rest()
            rested += 1

    logger.info(f"Sanity: {len(broken)} at 0 sanity, {rested} rested -> sanity={settings.sanity_max}")


def event_russian_roulette(casino: Casino) -> None:
    if getattr(casino, "is_bankrupt", False):
        return

    broke = _broke_players(casino)
    if len(broke) < 2:
        return

    p1, p2 = rnd.sample(broke, k=2)

    loser = p1 if rnd.random() < 0.5 else p2
    winner = p2 if loser is p1 else p1

    loser.die()
    logger.info(f"Russian Roulette: {p1.name} vs {p2.name} -> {loser.name} died")

    prize = 5000
    if casino.bankroll < prize:
        _mark_bankrupt(casino, f"can't pay russian roulette prize={prize}, bankroll={casino.bankroll:.2f}")
        return

    winner.balance += prize
    casino.bankroll -= prize
    _sync_balance(casino, winner)
    logger.info(f"Russian Roulette: {winner.name} won prize={prize} -> balance={winner.balance:.2f}")


def event_bankrupt(casino: Casino) -> None:
    _mark_bankrupt(casino, "forced bankrupt event")


RANDOM_EVENTS: list[Event] = [
    Event(name="roulette", handler=event_roulette, weight=1.0),
    Event(name="slots", handler=event_slots, weight=1.0),
    Event(name="honk_scream", handler=event_honk_scream, weight=0.8),
    Event(name="wargoose_attack", handler=event_wargoose_attack, weight=0.6),
]

MANDATORY_EVENTS: list[Event] = [
    Event(name="sanity_break", handler=event_sanity_break, weight=1.0),
    Event(name="russian_roulette", handler=event_russian_roulette, weight=1.0),
]


def call_mandatory_events(casino: Casino) -> None:
    if getattr(casino, "is_bankrupt", False):
        return
    if casino.bankroll <= 0:
        event_bankrupt(casino)
        return
    for e in MANDATORY_EVENTS:
        if getattr(casino, "is_bankrupt", False):
            return
        e.handler(casino)


def available_events(casino: Casino) -> list[Event]:
    if getattr(casino, "is_bankrupt", False):
        return []
    return [e for e in RANDOM_EVENTS if e.enabled(casino)]


def pick_event(casino: Casino, weighted: bool = True) -> Event:
    pool = available_events(casino)
    if not pool:
        raise RuntimeError("No events available")
    if not weighted:
        return rnd.choice(pool)
    return rnd.choices(pool, weights=[e.weight for e in pool], k=1)[0]
