import logging
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
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

# -------------------
# Enable CORS
# -------------------
origins = ["*"]  # In production, replace with your Streamlit app URL(s)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/forecast")
async def get_forecast(periods: int = Query(30, ge=1, le=365)):
    try:
        sales_data = load_sales_data()
        forecast_df = forecast_demand(sales_data, periods)
        return JSONResponse(content=forecast_df.to_dict(orient="records"))
    except Exception as e:
        logging.error(f"Error generating forecast: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/optimize_routes")
async def get_optimized_routes(
    num_vehicles: int = Query(1, ge=1, le=20),
    vehicle_capacity: int = Query(100, ge=1)
):
    try:
        locations_df = load_locations_data()
        routes = optimize_routes(locations_df, num_vehicles, vehicle_capacity)
        if routes is None:
            return JSONResponse(status_code=400, content={"error": "No feasible route solution found."})
        
        route_names = [[locations_df.iloc[idx]["name"] for idx in route] for route in routes]
        return {
            "routes_index": routes,
            "routes_names": route_names
        }
    except Exception as e:
        logging.error(f"Error optimizing routes: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is up.
    """
    return {"status": "ok"}
