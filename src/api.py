import logging
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from src.data_processing import load_sales_data, load_locations_data
from src.demand_forecasting import forecast_demand
from src.route_optimization import optimize_routes

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

app = FastAPI(
    title="AI-Powered Supply Chain Optimizer API",
    description="Forecast demand and optimize delivery routes using AI and OR-Tools.",
    version="1.0.0"
)

@app.get("/forecast")
async def get_forecast(periods: int = Query(30, ge=1, le=365, description="Future days to forecast")):
    """
    Generate demand forecast for the specified period using Prophet.
    """
    try:
        sales_data = load_sales_data()
        forecast_df = forecast_demand(sales_data, periods)
        return JSONResponse(content=forecast_df.to_dict(orient="records"))
    except Exception as e:
        logging.error(f"Error generating forecast: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/optimize_routes")
async def get_optimized_routes(
    num_vehicles: int = Query(1, ge=1, le=20, description="Number of delivery vehicles"),
    vehicle_capacity: int = Query(100, ge=1, description="Max packages per vehicle")
):
    """
    Optimize delivery routes using Google OR-Tools CVRP solver.
    """
    try:
        locations_df = load_locations_data()
        routes = optimize_routes(locations_df, num_vehicles, vehicle_capacity)
        if routes is None:
            return JSONResponse(status_code=400, content={"error": "No feasible route solution found."})
        
        route_names = []
        for route in routes:
            route_names.append([locations_df.iloc[idx]["name"] for idx in route])
        
        return {
            "routes_index": routes,
            "routes_names": route_names
        }
    except Exception as e:
        logging.error(f"Error optimizing routes: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
