from __future__ import annotations

from loguru import logger
from casino_lab4.collections.players import PlayerCollection
from casino_lab4.collections.geese import GooseCollection
from casino_lab4.collections.balances import Balance
from casino_lab4.domain.goose import Goose
from casino_lab4.domain.player import Player


class Casino:
    def __init__(self, bankroll: float) -> None:
        self.players = PlayerCollection()
        self.geese = GooseCollection()
        self.balances = Balance(user_naming="Player")
        self.geese_balances = Balance(user_naming="Goose")
        self.bankroll: float = bankroll
        self.is_bankrupt: bool = False

    def register_player(self, player: Player):
        self.players.append(player)
        self.balances[player.name] = player.balance
        logger.info(f"Player {player.name} registered with balance {player.balance}")

    def register_goose(self, goose: Goose):
        self.geese.append(goose)
        self.geese_balances[goose.name] = goose.balance
        logger.info(f"Goose {goose.name} registered with balance {goose.balance}")

    def unregister_player(self, player: Player):
        self.players.remove(player)
        del self.balances[player.name]
        logger.info(f"Player {player.name} unregistered")

    def unregister_goose(self, goose: Goose):
        self.geese.remove(goose)
        del self.geese_balances[goose.name]
        logger.info(f"Goose {goose.name} unregistered")
