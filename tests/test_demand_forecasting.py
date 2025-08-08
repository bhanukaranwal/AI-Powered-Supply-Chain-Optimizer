import pytest
from src.data_processing import load_sales_data
from src.demand_forecasting import forecast_demand
from src.utils import generate_synthetic_sales_data

# Ensure data exists
generate_synthetic_sales_data()

def test_forecast_demand():
    sales_data = load_sales_data()
    forecast = forecast_demand(sales_data, periods=15)
    
    assert "ds" in forecast.columns
    assert "yhat" in forecast.columns
    assert len(forecast) == len(sales_data) + 15
