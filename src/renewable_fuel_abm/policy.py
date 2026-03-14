"""Policy modules for pricing externalities."""

from dataclasses import dataclass


@dataclass
class CarbonPricePolicy:
    """Linear carbon price policy with price per emission unit."""

    carbon_price: float = 100.0

    def carbon_cost(self, emission_factor: float) -> float:
        """Return policy-induced cost per fuel unit."""

        return self.carbon_price * emission_factor
