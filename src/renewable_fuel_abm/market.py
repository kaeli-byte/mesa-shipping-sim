"""Market mechanics for fuel cost formation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping

from .policy import CarbonPricePolicy
from .scenario import FuelSpec


@dataclass
class MarketState:
    """Tracks delivered fuel prices by fuel type."""

    supplier_markup: Mapping[str, float]


def generalized_costs(
    fuels: Mapping[str, FuelSpec],
    policy: CarbonPricePolicy,
    market_state: MarketState,
) -> Dict[str, float]:
    """Compute generalized cost = base + supplier markup + carbon cost."""

    costs: Dict[str, float] = {}
    for fuel_name, spec in fuels.items():
        markup = market_state.supplier_markup.get(fuel_name, 0.0)
        costs[fuel_name] = spec.base_cost_per_unit + markup + policy.carbon_cost(spec.emission_factor)
    return costs
