import pytest
from src.data_processing import load_locations_data
from src.route_optimization import optimize_routes
from src.utils import generate_synthetic_locations

# Ensure locations file exists
generate_synthetic_locations()

def test_optimize_routes_basic():
    locations = load_locations_data()
    routes = optimize_routes(locations, num_vehicles=1, vehicle_capacity=200)

    assert routes is not None
    assert isinstance(routes, list)
    assert len(routes) == 1
    # Route must start and end at depot (index 0)
    assert routes[0][0] == 0
    assert routes[0][-1] == 0
