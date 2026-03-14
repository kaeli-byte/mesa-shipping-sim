# renewable-fuel-abm

A minimal Mesa-based agent-based model (ABM) for shipping fuel competition across:
- green methanol
- green ammonia
- green hydrogen
- fossil fuel

## v1 Features
- Mesa model with typed, src-based structure
- Agents:
  - `ShipOperatorAgent`
  - `FuelSupplierAgent`
  - `PortAgent`
  - `RegulatorAgent`
- Two shipping routes (`Asia-Europe`, `Transpacific`)
- Generalized fuel cost choice (base cost + supplier markup + carbon price cost)
- Carbon-price policy
- DataCollector outputs:
  - fleet fuel share
  - total emissions
  - average generalized cost

## Project layout

```text
.
├── configs/
├── scripts/
├── src/renewable_fuel_abm/
└── tests/
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Run simulation

```bash
python scripts/run_simulation.py --config configs/base.toml
python scripts/run_simulation.py --config configs/high_carbon_price.toml
```

## Run tests

```bash
pytest
```

## Extensibility notes
- Add richer supplier pricing behavior in `agents.py`
- Add route-specific demand growth in `scenario.py`
- Add dynamic policy pathways in `policy.py`
- Add additional KPIs in `metrics.py`
