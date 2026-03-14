from renewable_fuel_abm.model import ShippingFuelModel


def test_ship_operator_chooses_lowest_generalized_cost_fuel() -> None:
    model = ShippingFuelModel(num_ship_operators=2, carbon_price=250.0, seed=7)
    model.step()

    chosen_fuels = {agent.selected_fuel for agent in model.ship_operators}
    assert chosen_fuels == {"green_ammonia"}
