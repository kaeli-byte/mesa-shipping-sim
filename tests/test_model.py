from renewable_fuel_abm.model import ShippingFuelModel


def test_model_initializes_with_expected_agents() -> None:
    model = ShippingFuelModel(num_ship_operators=6)

    assert len(model.scenario.routes) == 2
    assert len(model.ship_operators) == 6
    assert model.policy.carbon_price == 120.0


def test_datacollector_has_expected_columns() -> None:
    model = ShippingFuelModel(num_ship_operators=4)
    model.step()

    frame = model.datacollector.get_model_vars_dataframe()
    assert {"fleet_share", "emissions", "average_cost"}.issubset(frame.columns)
