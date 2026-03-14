"""Scenario definitions for simulation setup."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Mapping, Sequence

FuelName = str


@dataclass(frozen=True)
class Route:
    """A shipping route with annual demand in energy units."""

    name: str
    annual_energy_demand: float


@dataclass(frozen=True)
class FuelSpec:
    """Fuel cost and emission factors."""

    name: FuelName
    base_cost_per_unit: float
    emission_factor: float


@dataclass(frozen=True)
class ScenarioConfig:
    """Top-level scenario definition."""

    routes: Sequence[Route]
    fuels: Mapping[FuelName, FuelSpec]


def default_scenario() -> ScenarioConfig:
    """Create a default v1 scenario with two routes and four fuels."""

    routes: List[Route] = [
        Route(name="Asia-Europe", annual_energy_demand=10_000.0),
        Route(name="Transpacific", annual_energy_demand=8_500.0),
    ]

    fuels: Dict[FuelName, FuelSpec] = {
        "green_methanol": FuelSpec("green_methanol", base_cost_per_unit=95.0, emission_factor=0.12),
        "green_ammonia": FuelSpec("green_ammonia", base_cost_per_unit=90.0, emission_factor=0.08),
        "green_hydrogen": FuelSpec("green_hydrogen", base_cost_per_unit=110.0, emission_factor=0.04),
        "fossil_fuel": FuelSpec("fossil_fuel", base_cost_per_unit=70.0, emission_factor=0.35),
    }

    return ScenarioConfig(routes=routes, fuels=fuels)
