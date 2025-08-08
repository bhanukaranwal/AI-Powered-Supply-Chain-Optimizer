import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_processing import load_sales_data, load_locations_data
from src.demand_forecasting import forecast_demand
from src.route_optimization import optimize_routes

st.set_page_config(
    page_title="AI-Powered Supply Chain Optimizer",
    layout="wide"
)

st.title("📦 AI-Powered Supply Chain Optimizer")

# -------------------------------
# Demand Forecast Section
# -------------------------------
st.header("📈 Demand Forecasting")

try:
    sales_data = load_sales_data()
    periods = st.slider("Forecast Periods (Days)", min_value=1, max_value=90, value=30, step=1)
    forecast = forecast_demand(sales_data, periods)

    fig = px.line(
        forecast, x="ds", y="yhat",
        labels={"ds": "Date", "yhat": "Predicted Demand"},
        title="Demand Forecast (Prophet)"
    )
    fig.add_scatter(
        x=sales_data["ds"], y=sales_data["y"],
        mode="lines", name="Historical Sales"
    )
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error loading/forecasting sales data: {e}")

# -------------------------------
# Delivery Route Optimization Section
# -------------------------------
st.header("🚚 Route Optimization")

try:
    locations = load_locations_data()
    num_vehicles = st.number_input("Number of Vehicles", min_value=1, max_value=10, value=1, step=1)
    vehicle_capacity = st.number_input("Vehicle Capacity", min_value=10, max_value=1000, value=100, step=10)

    if st.button("Optimize Routes"):
        with st.spinner("Optimizing, please wait..."):
            routes = optimize_routes(locations, num_vehicles, vehicle_capacity)

        if routes:
            st.subheader("Optimized Routes")
            for i, route in enumerate(routes):
                route_names = [locations.iloc[idx]["name"] for idx in route]
                st.write(f"Vehicle {i + 1}: {' → '.join(route_names)}")

            # Visualize on map
            fig_map = px.scatter_mapbox(
                locations, lat="latitude", lon="longitude", hover_name="name",
                zoom=10, height=500
            )
            for route in routes:
                route_locs = locations.iloc[route]
                fig_map.add_scattermapbox(
                    lat=route_locs["latitude"], lon=route_locs["longitude"],
                    mode="lines+markers", name=f"Route {routes.index(route) + 1}"
                )
            fig_map.update_layout(mapbox_style="open-street-map")
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.warning("No feasible route found for the given parameters.")
except Exception as e:
    st.error(f"Error loading or optimizing routes: {e}")
