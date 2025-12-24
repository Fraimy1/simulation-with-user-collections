from __future__ import annotations

import random as rnd

from casino_lab4.settings import settings
from casino_lab4.utils.logging import logger
from casino_lab4.simulation.setup import create_default_casino
from casino_lab4.simulation.events import pick_event, call_mandatory_events
from casino_lab4.simulation.stats import take_snapshot, compute_stats, print_statistics


def _is_simulation_over(casino) -> tuple[bool, str]:
    if getattr(casino, "is_bankrupt", False):
        return True, "Casino is bankrupt"

    if casino.bankroll <= 0:
        return True, "Casino has no money"

    alive_players = [p for p in casino.players if getattr(p, "alive", True)]
    if not alive_players:
        return True, "All players are dead"

    players_with_money = [p for p in alive_players if p.balance > 0]
    if not players_with_money:
        return True, "All players are broke"

    return False, ""


def run_simulation(steps: int | None = None, seed: int | None = None) -> None:
    if steps is None:
        steps = settings.simulation_steps
    if seed is None:
        seed = settings.simulation_seed
    if settings.use_seed and seed is not None:
        rnd.seed(seed)
        logger.info(f"Random seed set to: {seed}")

    logger.info("=" * 80)
    logger.info("CASINO SIMULATION START")
    logger.info("=" * 80)

    casino = create_default_casino()

    logger.info(f"Simulation parameters: steps={steps}, seed={seed}")
    logger.info(f"Casino initial bankroll: ${casino.bankroll:,.2f}")
    logger.info(f"Players: {len(casino.players)}")
    logger.info(f"Geese: {len(casino.geese)}")

    initial_snapshot = take_snapshot(casino)

    logger.info("=" * 80)
    logger.info("SIMULATION RUNNING")
    logger.info("=" * 80)

    for step in range(1, steps + 1):
        logger.info(f"\n--- STEP {step}/{steps} ---")

        is_over, reason = _is_simulation_over(casino)
        if is_over:
            logger.info(f"Simulation ended early: {reason}")
            break

        call_mandatory_events(casino)

        is_over, reason = _is_simulation_over(casino)
        if is_over:
            logger.info(f"Simulation ended after mandatory events: {reason}")
            break

        try:
            event = pick_event(casino, weighted=True)
            logger.info(f"Event: {event.name}")
            event.handler(casino)
        except RuntimeError as e:
            logger.info(f"No events available: {e}")
            break

        alive = sum(1 for p in casino.players if getattr(p, "alive", True))
        logger.info(
            f"Casino bankroll: ${casino.bankroll:,.2f} | Players alive: {alive}/{len(casino.players)}"
        )

    logger.info("\n" + "=" * 80)
    logger.info("SIMULATION COMPLETE")
    logger.info("=" * 80)

    final_snapshot = take_snapshot(casino)
    player_stats, goose_stats, casino_stats = compute_stats(
        initial_snapshot, final_snapshot
    )

    print_statistics(player_stats, goose_stats, casino_stats)
