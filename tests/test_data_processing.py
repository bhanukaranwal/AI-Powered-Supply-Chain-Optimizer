import pytest
import pandas as pd
from src.data_processing import load_sales_data, load_locations_data
from src.utils import generate_synthetic_sales_data, generate_synthetic_locations

# Generate sample data before tests
generate_synthetic_sales_data()
generate_synthetic_locations()

def test_load_sales_data():
    df = load_sales_data()
    assert isinstance(df, pd.DataFrame)
    assert "ds" in df.columns and "y" in df.columns
    assert pd.api.types.is_datetime64_any_dtype(df["ds"])
    assert len(df) > 0

def test_load_locations_data():
    df = load_locations_data()
    required_cols = ["location_id", "name", "latitude", "longitude", "demand"]
    for col in required_cols:
        assert col in df.columns
    assert len(df) > 0
