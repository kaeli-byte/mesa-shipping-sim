"""Core Mesa model for renewable shipping fuel competition."""

from __future__ import annotations

from typing import Dict, List

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

from .agents import FuelSupplierAgent, PortAgent, RegulatorAgent, ShipOperatorAgent
from .market import MarketState, generalized_costs
from .metrics import average_generalized_cost, fleet_share_by_fuel, total_emissions
from .policy import CarbonPricePolicy
from .scenario import Route, ScenarioConfig, default_scenario


class ShippingFuelModel(Model):
    """Simulates fuel adoption by shipping operators under policy and market conditions."""

    def __init__(
        self,
        num_ship_operators: int = 12,
        carbon_price: float = 120.0,
        scenario: ScenarioConfig | None = None,
        seed: int | None = 42,
    ) -> None:
        super().__init__(seed=seed)
        self.scenario = scenario or default_scenario()
        self.routes_by_name: Dict[str, Route] = {route.name: route for route in self.scenario.routes}
        self.policy = CarbonPricePolicy(carbon_price=carbon_price)
        self.schedule = RandomActivation(self)

        fuel_names = list(self.scenario.fuels.keys())
        self.supplier = FuelSupplierAgent(unique_id=1, model=self, fuels=fuel_names)
        self.regulator = RegulatorAgent(unique_id=2, model=self)
        self.ports: List[PortAgent] = [
            PortAgent(unique_id=3, model=self, name="Rotterdam", supported_fuels=fuel_names),
            PortAgent(unique_id=4, model=self, name="Singapore", supported_fuels=fuel_names),
        ]

        self.ship_operators: List[ShipOperatorAgent] = []
        route_names = [route.name for route in self.scenario.routes]
        for i in range(num_ship_operators):
            route_name = route_names[i % len(route_names)]
            operator = ShipOperatorAgent(unique_id=10 + i, model=self, route_name=route_name)
            self.ship_operators.append(operator)

        self._register_agents()

        self.datacollector = DataCollector(
            model_reporters={
                "fleet_share": lambda m: fleet_share_by_fuel(m),
                "emissions": lambda m: total_emissions(m),
                "average_cost": lambda m: average_generalized_cost(m),
            }
        )
        self.datacollector.collect(self)

    def _register_agents(self) -> None:
        self.schedule.add(self.regulator)
        self.schedule.add(self.supplier)
        for port in self.ports:
            self.schedule.add(port)
        for operator in self.ship_operators:
            self.schedule.add(operator)

    def current_generalized_costs(self) -> Dict[str, float]:
        """Get current generalized fuel costs across all fuels."""

        market_state = MarketState(supplier_markup=self.supplier.book.markups)
        return generalized_costs(self.scenario.fuels, self.policy, market_state)

    def step(self) -> None:
        self.schedule.step()
        self.datacollector.collect(self)
