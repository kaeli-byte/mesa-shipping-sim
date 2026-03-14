"""Metric helpers for reporting model outputs."""

from __future__ import annotations

from collections import Counter
from typing import Dict


def fleet_share_by_fuel(model: "ShippingFuelModel") -> Dict[str, float]:
    """Return fleet fuel shares for current timestep."""

    selections = [agent.selected_fuel for agent in model.ship_operators]
    counts = Counter(selections)
    total = len(selections) or 1
    return {fuel: count / total for fuel, count in counts.items()}


def total_emissions(model: "ShippingFuelModel") -> float:
    """Compute route-weighted emissions from selected fuels."""

    emissions = 0.0
    for operator in model.ship_operators:
        route = model.routes_by_name[operator.route_name]
        fuel = model.scenario.fuels[operator.selected_fuel]
        emissions += route.annual_energy_demand * fuel.emission_factor
    return emissions


def average_generalized_cost(model: "ShippingFuelModel") -> float:
    """Average selected fuel cost across fleet."""

    costs = model.current_generalized_costs()
    selected = [costs[agent.selected_fuel] for agent in model.ship_operators]
    return sum(selected) / (len(selected) or 1)


from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .model import ShippingFuelModel
