from database import fetch_energy_summary, fetch_generation_rate_data
import pandas as pd

def get_energy_summary(client_name: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetches the energy summary for the given client and date range.

    Args:
    - client_name (str): The name of the client.
    - start_date (str): The start date in 'YYYY-MM-DD' format.
    - end_date (str): The end date in 'YYYY-MM-DD' format.

    Returns:
    - pd.DataFrame: The energy summary data.
    """
    return fetch_energy_summary(client_name, start_date, end_date)

def get_generation_rate_data(du_name: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetches the generation rate data for the given DU and date range.

    Args:
    - du_name (str): The name of the distribution utility.
    - start_date (str): The start date in 'YYYY-MM-DD' format.
    - end_date (str): The end date in 'YYYY-MM-DD' format.

    Returns:
    - pd.DataFrame: The generation rate data.
    """
    return fetch_generation_rate_data(du_name, start_date, end_date)
