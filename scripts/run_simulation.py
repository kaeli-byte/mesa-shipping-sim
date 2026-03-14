#!/usr/bin/env python3
"""Run the renewable fuel ABM simulation from config."""

from __future__ import annotations

import argparse
import tomllib
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from renewable_fuel_abm.model import ShippingFuelModel


def load_config(path: Path) -> dict:
    with path.open("rb") as fh:
        return tomllib.load(fh)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run renewable fuel Mesa simulation")
    parser.add_argument("--config", type=Path, default=Path("configs/base.toml"))
    args = parser.parse_args()

    cfg = load_config(args.config)
    model = ShippingFuelModel(
        num_ship_operators=cfg.get("num_ship_operators", 12),
        carbon_price=cfg.get("carbon_price", 120.0),
        seed=cfg.get("seed", 42),
    )

    for _ in range(cfg.get("steps", 12)):
        model.step()

    results = model.datacollector.get_model_vars_dataframe().tail(1)
    print(results.to_string(index=False))


if __name__ == "__main__":
    main()
