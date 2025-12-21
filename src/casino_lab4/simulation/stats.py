from __future__ import annotations

from dataclasses import dataclass

from casino_lab4.simulation.casino import Casino
from casino_lab4.domain.player import Player
from casino_lab4.domain.goose import Goose


@dataclass
class PlayerStats:
    name: str
    initial_balance: float
    final_balance: float
    initial_sanity: int
    final_sanity: int
    alive: bool
    
    @property
    def balance_change(self) -> float:
        return self.final_balance - self.initial_balance
    
    @property
    def sanity_change(self) -> int:
        return self.final_sanity - self.initial_sanity


@dataclass
class GooseStats:
    name: str
    goose_type: str
    initial_balance: float
    final_balance: float
    honk_volume: float
    
    @property
    def balance_change(self) -> float:
        return self.final_balance - self.initial_balance


@dataclass
class CasinoStats:
    initial_bankroll: float
    final_bankroll: float
    is_bankrupt: bool
    
    @property
    def bankroll_change(self) -> float:
        return self.final_bankroll - self.initial_bankroll


@dataclass
class SimulationSnapshot:
    players: dict[str, tuple[float, int, bool]]
    geese: dict[str, tuple[float, str]]
    casino_bankroll: float


def take_snapshot(casino: Casino) -> SimulationSnapshot:
    players = {
        p.name: (float(p.balance), int(p.sanity), bool(getattr(p, "alive", True)))
        for p in casino.players
    }
    
    geese = {
        g.name: (float(g.balance), type(g).__name__)
        for g in casino.geese
    }
    
    return SimulationSnapshot(
        players=players,
        geese=geese,
        casino_bankroll=float(casino.bankroll)
    )


def compute_stats(initial: SimulationSnapshot, final: SimulationSnapshot) -> tuple[list[PlayerStats], list[GooseStats], CasinoStats]:
    player_stats = []
    for name, (init_balance, init_sanity, init_alive) in initial.players.items():
        if name in final.players:
            fin_balance, fin_sanity, fin_alive = final.players[name]
        else:
            fin_balance, fin_sanity, fin_alive = init_balance, init_sanity, init_alive
        
        player_stats.append(PlayerStats(
            name=name,
            initial_balance=init_balance,
            final_balance=fin_balance,
            initial_sanity=init_sanity,
            final_sanity=fin_sanity,
            alive=fin_alive
        ))
    
    goose_stats = []
    for name, (init_balance, goose_type) in initial.geese.items():
        if name in final.geese:
            fin_balance, _ = final.geese[name]
        else:
            fin_balance = init_balance
        
        goose_stats.append(GooseStats(
            name=name,
            goose_type=goose_type,
            initial_balance=init_balance,
            final_balance=fin_balance,
            honk_volume=0.0
        ))
    
    casino_stats = CasinoStats(
        initial_bankroll=initial.casino_bankroll,
        final_bankroll=final.casino_bankroll,
        is_bankrupt=final.casino_bankroll <= 0
    )
    
    return player_stats, goose_stats, casino_stats


def print_statistics(player_stats: list[PlayerStats], goose_stats: list[GooseStats], casino_stats: CasinoStats) -> None:
    from casino_lab4.utils.logging import logger
    
    logger.info("=" * 80)
    logger.info("SIMULATION STATISTICS")
    logger.info("=" * 80)
    
    logger.info(f"\nCASINO:")
    logger.info(f"  Initial Bankroll: ${casino_stats.initial_bankroll:,.2f}")
    logger.info(f"  Final Bankroll:   ${casino_stats.final_bankroll:,.2f}")
    logger.info(f"  Change:           ${casino_stats.bankroll_change:+,.2f}")
    logger.info(f"  Status:           {'BANKRUPT' if casino_stats.is_bankrupt else 'OPERATING'}")
    
    logger.info(f"\nPLAYERS ({len(player_stats)}):")
    for ps in player_stats:
        status = "DEAD" if not ps.alive else "ALIVE"
        logger.info(f"  {ps.name}:")
        logger.info(f"    Balance: ${ps.initial_balance:,.2f} -> ${ps.final_balance:,.2f} ({ps.balance_change:+,.2f})")
        logger.info(f"    Sanity:  {ps.initial_sanity} -> {ps.final_sanity} ({ps.sanity_change:+d})")
        logger.info(f"    Status:  {status}")
    
    logger.info(f"\nGEESE ({len(goose_stats)}):")
    for gs in goose_stats:
        logger.info(f"  {gs.name} ({gs.goose_type}):")
        logger.info(f"    Balance: ${gs.initial_balance:,.2f} -> ${gs.final_balance:,.2f} ({gs.balance_change:+,.2f})")
    
    total_player_change = sum(ps.balance_change for ps in player_stats)
    alive_players = sum(1 for ps in player_stats if ps.alive)
    dead_players = len(player_stats) - alive_players
    
    logger.info(f"\nSUMMARY:")
    logger.info(f"  Total Player Wealth Change: ${total_player_change:+,.2f}")
    logger.info(f"  Players Alive: {alive_players}/{len(player_stats)}")
    logger.info(f"  Players Dead:  {dead_players}/{len(player_stats)}")
    logger.info(f"  Casino Status: {'BANKRUPT' if casino_stats.is_bankrupt else 'OPERATING'}")
    
    logger.info("=" * 80)

