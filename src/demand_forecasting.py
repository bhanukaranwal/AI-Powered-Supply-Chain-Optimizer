import logging
from prophet import Prophet
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def forecast_demand(sales_data: pd.DataFrame, periods: int = 30) -> pd.DataFrame:
    """
    Forecast product demand using Prophet.

    Parameters:
        sales_data (pd.DataFrame): DataFrame with 'ds' (date) and 'y' (sales) columns.
        periods (int): Number of future days to forecast.

    Returns:
        pd.DataFrame: Forecast results with columns ['ds', 'yhat', 'yhat_lower', 'yhat_upper'].
    """
    # Validate input
    if not isinstance(sales_data, pd.DataFrame):
        logging.error("sales_data must be a pandas DataFrame.")
        raise TypeError("sales_data must be a pandas DataFrame.")

    if "ds" not in sales_data.columns or "y" not in sales_data.columns:
        logging.error("sales_data missing required columns 'ds' and 'y'.")
        raise ValueError("sales_data must have 'ds' and 'y' columns for forecasting.")

    # Fit Prophet model
    logging.info("Starting demand forecasting using Prophet...")
    model = Prophet(yearly_seasonality=True,
                   weekly_seasonality=True,
                   daily_seasonality=False)

    try:
        model.fit(sales_data)
    except Exception as e:
        logging.error(f"Error fitting Prophet model: {e}")
        raise

    # Create future dates & predict
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    logging.info(f"Forecast completed for {periods} future days.")
    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
