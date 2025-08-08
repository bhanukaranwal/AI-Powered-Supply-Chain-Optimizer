import logging
import pandas as pd
from ortools.constraint_solver import routing_enums_pb2, pywrapcp
from src.utils import haversine_distance

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def optimize_routes(locations: pd.DataFrame, num_vehicles: int = 1, vehicle_capacity: int = 100):
    """
    Optimize delivery routes using Google OR-Tools capacitated vehicle routing problem (CVRP).

    Parameters:
        locations (pd.DataFrame): must contain ['location_id', 'latitude', 'longitude', 'demand'].
        num_vehicles (int): number of delivery vehicles available.
        vehicle_capacity (int): maximum units each vehicle can carry.

    Returns:
        list[list[int]]: Routes per vehicle (list of location indices in visiting order).
                         Locations are indexed as in the DataFrame.
                         Example: [[0, 2, 1, 0], [0, 3, 4, 0]]
    """

    # Validate input
    required_cols = ["location_id", "latitude", "longitude", "demand"]
    if not all(col in locations.columns for col in required_cols):
        logging.error(f"Locations DataFrame must contain columns: {required_cols}")
        raise ValueError(f"Missing required columns: {required_cols}")

    n = len(locations)
    if n < 2:
        logging.error("Need at least 2 locations (depot + 1 customer) for optimization.")
        raise ValueError("Not enough locations for routing.")

    logging.info(f"Optimizing routes for {n} locations, {num_vehicles} vehicles, capacity {vehicle_capacity}.")

    # Build distance matrix (in meters)
    distances = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                distances[i][j] = int(haversine_distance(
                    locations.iloc[i]["latitude"], locations.iloc[i]["longitude"],
                    locations.iloc[j]["latitude"], locations.iloc[j]["longitude"]
                ) * 1000)  # km -> meters

    # Demands
    demands = locations["demand"].tolist()

    # OR-Tools manager & routing model
    manager = pywrapcp.RoutingIndexManager(n, num_vehicles, 0)  # 0 = depot
    routing = pywrapcp.RoutingModel(manager)

    # Distance callback
    def distance_callback(from_idx, to_idx):
        from_node = manager.IndexToNode(from_idx)
        to_node = manager.IndexToNode(to_idx)
        return distances[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add capacity constraint
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return demands[from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(demand_callback_index, 0, [vehicle_capacity] * num_vehicles,
                                            True, "Capacity")

    # Set search parameters
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    search_parameters.time_limit.seconds = 10  # limit for larger problems

    # Solve
    solution = routing.SolveWithParameters(search_parameters)

    if not solution:
        logging.warning("No feasible routing solution found for the given parameters.")
        return None

    # Extract routes
    routes = []
    for vehicle_id in range(num_vehicles):
        index = routing.Start(vehicle_id)
        route = []
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))  # return to depot
        routes.append(route)

    logging.info(f"Routing optimization complete. Generated {len(routes)} routes.")
    return routes
