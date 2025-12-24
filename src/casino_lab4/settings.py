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
    honk_fear_fee_pct: float = 0.05
    honk_fear_fee_max: float = 50.0

    russian_roulette_prize: float = 5000.0

    simulation_steps: int = 100
    simulation_seed: int = 42
    use_seed: bool = True

    wargoose_attack_victims_min: int = 1
    wargoose_attack_victims_max: int = 3
    wargoose_steal_pct_min: float = 0.30
    wargoose_steal_pct_max: float = 0.50

    chip_denominations: tuple[int, ...] = (1, 5, 25, 50, 100)

    roulette_user_choice_probabilities: dict[str, float] = Field(
        default_factory=lambda: {
            "0": 0.05,
            "00": 0.05,
            "red": 0.45,
            "black": 0.45,
        }
    )

    roulette_payout_total: dict[str, int] = Field(
        default_factory=lambda: {
            "0": 36,
            "00": 36,
            "red": 2,
            "black": 2,
        }
    )

    slot_probabilities: dict[str, float] = Field(
        default_factory=lambda: {
            "777": 0.05,
            "JACKPOT_25": 0.10,
            "JACKPOT_15": 0.15,
            "JACKPOT_10": 0.20,
            "MISS": 0.50,
        }
    )

    slot_payout_total: dict[str, int] = Field(
        default_factory=lambda: {
            "777": 8,
            "JACKPOT_25": 2,
            "JACKPOT_15": 1,
            "JACKPOT_10": 1,
            "MISS": 0,
        }
    )

    slot_sanity_delta: dict[str, int] = Field(
        default_factory=lambda: {
            "777": +50,
            "JACKPOT_25": +25,
            "JACKPOT_15": +10,
            "JACKPOT_10": +10,
            "MISS": -20,
        }
    )

    @model_validator(mode="after")
    def _validate(self) -> "Settings":
        if (
            self.roulette_green_slots
            + self.roulette_red_slots
            + self.roulette_black_slots
            != self.roulette_total_slots
        ):
            raise ValueError("Roulette slots must sum to roulette_total_slots")

        if self.roulette_green_slots not in (1, 2):
            raise ValueError(
                "roulette_green_slots must be 1 (european) or 2 (american)"
            )

        if any(p < 0 for p in self.roulette_user_choice_probabilities.values()):
            raise ValueError("roulette_user_choice_probabilities must be non-negative")
        if abs(sum(self.roulette_user_choice_probabilities.values()) - 1.0) > 1e-9:
            raise ValueError("roulette_user_choice_probabilities must sum to 1")

        if any(p < 0 for p in self.slot_probabilities.values()):
            raise ValueError("slot_probabilities must be non-negative")
        if abs(sum(self.slot_probabilities.values()) - 1.0) > 1e-9:
            raise ValueError("slot_probabilities must sum to 1")

        return self

    @cached_property
    def roulette_green_outcomes(self) -> tuple[str, ...]:
        return ("0",) if self.roulette_green_slots == 1 else ("0", "00")

    @cached_property
    def roulette_probabilities(self) -> dict[str, float]:
        total = float(self.roulette_total_slots)
        probs: dict[str, float] = {k: 1.0 / total for k in self.roulette_green_outcomes}
        probs["red"] = self.roulette_red_slots / total
        probs["black"] = self.roulette_black_slots / total
        return probs

    @cached_property
    def roulette_outcomes(self) -> list[str]:
        return list(self.roulette_probabilities.keys())

    @cached_property
    def roulette_weights(self) -> list[float]:
        return list(self.roulette_probabilities.values())

    @cached_property
    def roulette_user_choice_outcomes(self) -> list[str]:
        return list(self.roulette_user_choice_probabilities.keys())

    @cached_property
    def roulette_user_choice_weights(self) -> list[float]:
        return list(self.roulette_user_choice_probabilities.values())

    @cached_property
    def roulette_payout_keys(self) -> list[str]:
        return list(self.roulette_payout_total.keys())

    @cached_property
    def roulette_payout_values(self) -> list[int]:
        return list(self.roulette_payout_total.values())

    @cached_property
    def slot_outcomes(self) -> list[str]:
        return list(self.slot_probabilities.keys())

    @cached_property
    def slot_weights(self) -> list[float]:
        return list(self.slot_probabilities.values())

    @cached_property
    def slot_payout_keys(self) -> list[str]:
        return list(self.slot_payout_total.keys())

    @cached_property
    def slot_payout_values(self) -> list[int]:
        return list(self.slot_payout_total.values())


settings = Settings()
