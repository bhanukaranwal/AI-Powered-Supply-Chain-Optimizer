import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, atan2
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def generate_synthetic_sales_data(start_date="2024-01-01", days=365, file_path="data/historical_sales.csv"):
    """Generate synthetic sales data with weekly seasonality + noise."""
    os.makedirs("data", exist_ok=True)
    dates = [datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i) for i in range(days)]
    seasonal_pattern = np.sin(np.arange(days) * 2 * np.pi / 7) * 15  # weekly
    sales = np.random.normal(loc=100, scale=10, size=days) + seasonal_pattern
    sales = np.clip(sales, 50, None)  # prevent negative
    df = pd.DataFrame({"ds": dates, "y": sales})
    df.to_csv(file_path, index=False)
    logging.info(f"Synthetic sales data saved to {file_path}")
    return df


def generate_synthetic_locations(num_locations=5, file_path="data/locations.csv"):
    """Generate synthetic store locations around NYC."""
    os.makedirs("data", exist_ok=True)
    data = {
        "location_id": list(range(num_locations)),
        "name": ["Warehouse"] + [f"Store{i}" for i in range(1, num_locations)],
        "latitude": [40.7128] + np.random.uniform(40.6, 40.8, num_locations-1).tolist(),
        "longitude": [-74.0060] + np.random.uniform(-74.1, -73.9, num_locations-1).tolist(),
        "demand": [0] + np.random.randint(10, 60, num_locations-1).tolist()
    }
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    logging.info(f"Synthetic locations saved to {file_path}")
    return df


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate haversine distance in kilometers."""
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return R * (2 * atan2(sqrt(a), sqrt(1 - a)))
