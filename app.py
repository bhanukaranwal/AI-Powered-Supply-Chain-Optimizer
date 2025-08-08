import os
import requests
import streamlit as st
import pandas as pd
import plotly.express as px

# Local imports for direct Python calls if running without backend API
from src.data_processing import load_sales_data, load_locations_data
from src.demand_forecasting import forecast_demand
from src.route_optimization import optimize_routes

# -------------------
# Configurable base URL
# -------------------
API_URL = os.getenv("API_URL", "http://localhost:8000")  # default when running locally

st.set_page_config(page_title="AI-Powered Supply Chain Optimizer", layout="wide")
st.title("📦 AI-Powered Supply Chain Optimizer")

# -------------------
# Demand Forecast via API
# -------------------
st.header("📈 Demand Forecasting")
periods = st.slider("Forecast Periods (Days)", 1, 90, 30)

if st.button("Get Forecast from API"):
    try:
        resp = requests.get(f"{API_URL}/forecast", params={"periods": periods})
        if resp.status_code == 200:
            forecast = pd.DataFrame(resp.json())
            sales_data = load_sales_data()
            
            fig = px.line(forecast, x="ds", y="yhat", title="Demand Forecast", labels={"yhat": "Predicted Demand"})
            fig.add_scatter(x=sales_data["ds"], y=sales_data["y"], mode="lines", name="Historical Sales")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(f"API Error: {resp.status_code} - {resp.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")

# -------------------
# Route Optimization via API
# -------------------
st.header("🚚 Route Optimization")
num_vehicles = st.number_input("Number of Vehicles", min_value=1, max_value=10, value=1)
vehicle_capacity = st.number_input("Vehicle Capacity", min_value=10, max_value=1000, value=100)

if st.button("Optimize Routes via API"):
    try:
        resp = requests.get(f"{API_URL}/optimize_routes", params={
            "num_vehicles": num_vehicles,
            "vehicle_capacity": vehicle_capacity
        })
        if resp.status_code == 200:
            data = resp.json()
            st.write("Routes (by location name):")
            for i, route in enumerate(data["routes_names"]):
                st.write(f"Vehicle {i+1}: {' → '.join(route)}")

            # Plot map
            locations = load_locations_data()
            fig_map = px.scatter_mapbox(locations, lat="latitude", lon="longitude", text="name", zoom=10)
            for route in data["routes_index"]:
                route_locs = locations.iloc[route]
                fig_map.add_scattermapbox(lat=route_locs["latitude"], lon=route_locs["longitude"], mode="lines+markers")
            fig_map.update_layout(mapbox_style="open-street-map")
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.error(f"API Error: {resp.status_code} - {resp.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")
