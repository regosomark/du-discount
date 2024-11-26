import pandas as pd
from database import fetch_client_load_profile, fetch_generation_rate_data

def get_client_load_profile(client_name: str, start_date: str, end_date: str):
    return fetch_client_load_profile(client_name, start_date, end_date)

def get_generation_rate_data(du_name: str, start_date: str, end_date: str):
    return fetch_generation_rate_data(du_name, start_date, end_date)

def combine_data(energy_summary: pd.DataFrame, rate_data: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and merges the energy_summary DataFrame with rate_data based on supply_period.
    - Removes rows with 'Total', 'Average', 'Max', or 'Min' in 'supply_period'.
    - Merges the data on 'supply_period'.
    - Fills missing generation_rate values using forward fill.
    - Fills remaining missing generation_rate values with a default value (0).
    
    Parameters:
        energy_summary (pd.DataFrame): The client energy summary data.
        rate_data (pd.DataFrame): The generation rate data to merge with energy_summary.
    
    Returns:
        pd.DataFrame: The cleaned and merged DataFrame with relevant columns.
    """
    # Remove rows with invalid 'supply_period' values first
    invalid_periods = ['Total', 'Average', 'Max', 'Min']
    energy_summary = energy_summary[~energy_summary['supply_period'].isin(invalid_periods)]
    
    # Convert 'supply_period' columns to date type for consistency
    energy_summary['supply_period'] = pd.to_datetime(energy_summary['supply_period']).dt.date
    rate_data['supply_period'] = pd.to_datetime(rate_data['supply_period']).dt.date
    
    # Merge energy_summary with rate_data on 'supply_period' using left join
    merged_df = energy_summary.merge(rate_data, on="supply_period", how="left")
    
    # Fill missing generation_rate values with the previous available generation_rate (forward fill)
    merged_df['generation_rate'] = merged_df['generation_rate'].fillna(method='ffill')
    
    # If there's still any missing generation_rate (in case of the first row), fill with default value (e.g., 0)
    merged_df['generation_rate'] = merged_df['generation_rate'].fillna(0)
    
    # Return the cleaned and merged DataFrame with relevant columns
    result_df = merged_df[['supply_period', 'kwh', 'generation_rate']]
    
    return result_df