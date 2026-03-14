"""Agent definitions for shipping fuel competition."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List

from mesa import Agent


class ShipOperatorAgent(Agent):
    """Chooses fuel based on lowest generalized cost on assigned route."""

    def __init__(self, unique_id: int, model: "ShippingFuelModel", route_name: str) -> None:
        super().__init__(unique_id, model)
        self.route_name = route_name
        self.selected_fuel: str = "fossil_fuel"

    def step(self) -> None:
        costs = self.model.current_generalized_costs()
        self.selected_fuel = min(costs, key=costs.get)


@dataclass
class SupplierBook:
    """Tracks supplier markup decisions."""

    markups: Dict[str, float] = field(default_factory=dict)


class FuelSupplierAgent(Agent):
    """Provides markups for fuels in a simple competitive market."""

    def __init__(self, unique_id: int, model: "ShippingFuelModel", fuels: Iterable[str]) -> None:
        super().__init__(unique_id, model)
        self.book = SupplierBook({fuel: 0.0 for fuel in fuels})

    def step(self) -> None:
        # Minimal behavior for v1: keep neutral markups.
        for fuel in self.book.markups:
            self.book.markups[fuel] = 0.0


class PortAgent(Agent):
    """Represents infrastructure availability for fuels."""

    def __init__(self, unique_id: int, model: "ShippingFuelModel", name: str, supported_fuels: List[str]) -> None:
        super().__init__(unique_id, model)
        self.name = name
        self.supported_fuels = supported_fuels

    def step(self) -> None:
        # Placeholder for future infrastructure expansion rules.
        return


class RegulatorAgent(Agent):
    """Maintains policy settings for the market."""

    def __init__(self, unique_id: int, model: "ShippingFuelModel") -> None:
        super().__init__(unique_id, model)

    def step(self) -> None:
        # v1 uses fixed carbon price, but this hook supports dynamic policy later.
        return


# Avoid circular imports at runtime for typing
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .model import ShippingFuelModel
