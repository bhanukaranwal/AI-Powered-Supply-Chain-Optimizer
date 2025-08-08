import pandas as pd
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def load_sales_data(file_path="data/historical_sales.csv"):
    """
    Load and preprocess sales data for forecasting.
    Returns a DataFrame with columns: ds (datetime), y (sales).
    """
    if not os.path.exists(file_path):
        logging.error(f"Sales data file {file_path} not found.")
        raise FileNotFoundError(f"Sales data file {file_path} does not exist.")
    
    df = pd.read_csv(file_path)
    if "ds" not in df.columns or "y" not in df.columns:
        logging.error("Invalid sales data format: 'ds' and 'y' columns required.")
        raise ValueError("Sales data must contain 'ds' and 'y' columns.")

    df["ds"] = pd.to_datetime(df["ds"], errors="coerce")
    if df["ds"].isnull().any():
        logging.warning("Some dates could not be parsed and will be dropped.")
        df = df.dropna(subset=["ds"])
    
    logging.info(f"Loaded {len(df)} rows of sales data from {file_path}")
    return df


def load_locations_data(file_path="data/locations.csv"):
    """
    Load and preprocess location data for route optimization.
    Expected columns: location_id, name, latitude, longitude, demand.
    """
    if not os.path.exists(file_path):
        logging.error(f"Locations data file {file_path} not found.")
        raise FileNotFoundError(f"Locations data file {file_path} does not exist.")

    df = pd.read_csv(file_path)
    required_cols = ["location_id", "name", "latitude", "longitude", "demand"]
    if not all(col in df.columns for col in required_cols):
        logging.error(f"Invalid locations file format: missing required columns {required_cols}")
        raise ValueError(f"Locations file must contain {required_cols}")

    logging.info(f"Loaded {len(df)} locations from {file_path}")
    return df
