from __future__ import annotations

from functools import cached_property
from typing import Literal

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="CASINO_",
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    roulette_wheel: Literal["american", "european"] = "american"

    roulette_total_slots: int = 38
    roulette_green_slots: int = 2
    roulette_red_slots: int = 18
    roulette_black_slots: int = 18

    slot_spin_cost: int = 20

    player_start_cash_min: int = 200
    player_start_cash_max: int = 2000

    sanity_max: int = 100
    sanity_skip_turn_chance: float = 0.8
    sanity_act_anyway_chance: float = 0.2

    honk_sanity_debuff: int = 10

    wargoose_attack_victims_min: int = 1
    wargoose_attack_victims_max: int = 3
    wargoose_steal_pct_min: float = 0.30
    wargoose_steal_pct_max: float = 0.50

    chip_denominations: tuple[int, ...] = (1, 5, 25, 50, 100)

    @model_validator(mode="after")
    def _validate_roulette(self) -> "Settings":
        if self.roulette_green_slots + self.roulette_red_slots + self.roulette_black_slots != self.roulette_total_slots:
            raise ValueError("Roulette slots must sum to roulette_total_slots")
        return self

    @cached_property
    def roulette_probabilities(self) -> dict[str, float]:
        total = float(self.roulette_total_slots)
        return {
            "0": 1 / total,
            "00": 1 / total,
            "red": self.roulette_red_slots / total,
            "black": self.roulette_black_slots / total,
        }

    @cached_property
    def roulette_outcomes(self) -> list[str]:
        return list(self.roulette_probabilities.keys())

    @cached_property
    def roulette_weights(self) -> list[float]:
        return list(self.roulette_probabilities.values())

    @cached_property
    def roulette_user_choice_weights(self) -> list[float]:
        return {
            "0": 0.05,
            "00": 0.05,
            "red": 0.45,
            "black": 0.45,
        }
    
    @cached_property
    def roulette_user_choice_weights(self) -> list[float]:
        return list(self.roulette_user_choice_weights.values())

    @cached_property
    def roulette_user_choice_outcomes(self) -> list[str]:
        return list(self.roulette_user_choice_weights.keys())

    @cached_property
    def roulette_payouts(self) -> list[float]:
        return {
            "0": 36,
            "00": 36,
            "red": 2,
            "black": 2,
        }
    
    @cached_property
    def roulette_payout_values(self) -> list[float]:
        return list(self.roulette_user_choice_weights.values())

    @cached_property
    def roulette_payout_keys(self) -> list[str]:
        return list(self.roulette_user_choice_weights.keys())

    @cached_property
    def slot_payouts(self) -> list[float]:
        return {
            "777": 8,
            "JACKPOT-25": 2,
            "JACKPOT-15": 1,
            "JACKPOT-10": 1,
            "MISS": 0
        }
    
    @cached_property
    def slot_sanity_gain(self) -> list[float]:
        return {
            "777": +50,
            "JACKPOT-25": +25,
            "JACKPOT-15": +10,
            "JACKPOT-10": +10,
            "MISS": -20
        }
    
    

settings = Settings()
