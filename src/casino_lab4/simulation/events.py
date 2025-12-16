from __future__ import annotations

import random as rnd

from casino_lab4.settings import settings
from casino_lab4.simulation.casino import Casino
from casino_lab4.simulation.event_types import Event
from casino_lab4.simulation.selectors import select_players
from casino_lab4.utils.logging import logger

from casino_lab4.domain.goose import HonkGoose, WarGoose
from casino_lab4.domain.player import Player

def _sync_balance(casino: Casino, player:Player) -> None:
    casino.balances[player.name] = float(player.balance)

#TODO: Make select_players be called outside the functions

def _roulette_roll() -> str:
    return rnd.choices(
        population=settings.roulette_outcomes,
        weights=settings.roulette_weights,
        k=1,
    )[0]


def event_roulette(casino: Casino) -> None:
    players = list(select_players(casino, min_balance=1))
    if not players:
        logger.info("Roulette: no players selected")
        return

    for player in players:  
        bet = rnd.randint(1, max(1, min(int(player.balance), 100)))
        user_choice = rnd.choices(settings.roulette_user_choice_outcomes(), weights=settings.roulette_user_choice_weights(), k=1)[0]
        casino_choice = _roulette_roll()

        player.balance -= bet
        casino.bankroll += bet
        _sync_balance(casino, player)

        if casino_choice == user_choice:
            roullete_payouts = settings.roulette_payouts()

            payout = bet * roullete_payouts[user_choice]
            
            if casino.bankroll < payout:
                logger.info(f"Roulette: casino can't pay {player.name} (needed {payout})")
                casino.is_bankrupt = True
                return

            player.balance += payout
            casino.bankroll -= payout
            #TODO: Add sanity logic to this
            _sync_balance(casino, player)
            logger.info(
                f"Roulette: {player.name} bet {bet} on {user_choice}, roll={casino_choice} -> WIN (+{bet})"
            )    
        else:
            logger.info(
                f"Roulette: {player.name} bet {bet} on {user_choice}, roll={casino_choice} -> LOSE (-{bet})"
            )

def _slots_pull(casino: Casino, player: Player, cost: int) -> str:
    slot_sanity_gains = settings.slot_sanity_gain()
    slot_payouts = settings.slot_payouts()
    
    player.balance -= cost
    casino.bankroll += cost
    _sync_balance(casino, player)

    r = rnd.random()

    if r < 0.05:
        label = "777"
    elif r < 0.15:
        label = "JACKPOT-25"
    elif r < 0.30:
        label = "JACKPOT-15"
    elif r < 0.50:
        label = "JACKPOT-10"
    else:
        label = "MISS"
    payout = slot_payouts[label]
    sanity_gain = slot_sanity_gains[label]
    
    player.apply_sanity(player.sanity + sanity_gain)
    player.balance += cost * payout
    casino.bankroll -= cost * payout
    _sync_balance(casino, player)

    return label


def event_slots(casino: Casino) -> None:
    cost = settings.slot_spin_cost

    players = list(select_players(casino, cost))
    if not players:
        logger.info("Slots: no players selected")
        return
    
    for player in players:
        pulls_number = rnd.randint(0, player.balance % cost)
        n_wins = 0
        for _ in range(pulls_number):
            label = _slots_pull(casino, player, cost)
            if label != "MISS":
                n_wins += 1
        
        logger.info(f"Slots: {player.name} pulled {pulls_number} times, {n_wins} wins -> balance={player.balance:.2f}")


def event_honk_scream(casino: Casino) -> None:
    geese = [g for g in casino.geese if isinstance(g, HonkGoose)]
    players = list(select_players(casino))

    if not geese or not players:
        logger.info("Honk: no HonkGoose or no players selected")
        return

    goose = rnd.choice(geese)
    debuff = int(goose.scream())

    affected = 0
    for p in players:
        p.apply_sanity(p.sanity - debuff)
        affected += 1

    logger.info(f"Honk: {goose.name} screamed -> sanity -{debuff} to {affected} player(s)")


def event_wargoose_attack(casino: Casino) -> None:
    geese = [g for g in casino.geese if isinstance(g, WarGoose)]
    players = list(select_players(casino, 1))

    if not geese or not players:
        logger.info("Attack: no WarGoose or no players")
        return

    goose = rnd.choice(geese)

    k_min = int(getattr(settings, "wargoose_attack_victims_min", 1))
    k_max = int(getattr(settings, "wargoose_attack_victims_max", 3))
    k = max(1, min(len(players), rnd.randint(k_min, k_max)))

    victims = rnd.sample(players, k=k)
    total = 0.0

    for v in victims:
        if v.balance <= 0:
            continue

        stolen = 0.0

        stolen = float(goose.attack(v))  

        stolen = max(0.0, float(stolen))
        total += stolen
        casino.bankroll += stolen #TODO for now goes to casino, should go to geese
        _sync_balance(casino, v)

    logger.info(f"Attack: {goose.name} attacked {len(victims)} player(s), total stolen={total:.2f}")


def event_sanity_break(casino: Casino) -> None:
    players = list(select_players(casino, 0))
    if not players:
        logger.info("Sanity: no players")
        return

    broken = [p for p in players if p.sanity <= 0]
    if not broken:
        logger.info("Sanity: no breakdowns")
        return

    skip_p = settings.sanity_skip_turn_chance
    rested = 0

    for p in broken:
        if rnd.random() < skip_p:
            p.rest()
            rested += 1
            logger.info(f"Sanity: {p.name} rested")
        else:
            logger.info(f"Sanity: {p.name} skipped turn")

    logger.info(f"Sanity: {len(broken)} at 0 sanity, {rested} rested -> sanity=100")


RANDOM_EVENTS: list[Event] = [
    Event(name="roulette", handler=event_roulette, weight=1.0),
    Event(name="slots", handler=event_slots, weight=1.0),
    Event(name="honk_scream", handler=event_honk_scream, weight=0.8),
    Event(name="wargoose_attack", handler=event_wargoose_attack, weight=0.6),
]

MANDATORY_EVENTS: list[Event] = [
    Event(name="sanity_break", handler=event_sanity_break, weight=1.0),
]

def available_events(casino: Casino) -> list[Event]:
    return [e for e in RANDOM_EVENTS if e.enabled(casino)]


def pick_event(casino: Casino, weighted: bool = True) -> Event:
    pool = available_events(casino)
    if not pool:
        raise RuntimeError("No events available")
    if not weighted:
        return rnd.choice(pool)
    return rnd.choices(pool, weights=[e.weight for e in pool], k=1)[0]
