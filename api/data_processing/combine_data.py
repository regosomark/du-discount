import pandas as pd

def combine_data(energy_summary, generation_rate_data):
    # Clean and merge data
    energy_summary['supply_period'] = pd.to_datetime(energy_summary['supply_period'], format='%Y-%m')
    generation_rate_data['supply_period'] = pd.to_datetime(generation_rate_data['supply_period'], format='%Y-%m')
    
    # Merge on supply_period
    merged_df = pd.merge(energy_summary, generation_rate_data, on='supply_period', how='left')
    merged_df['generation_rate'] = merged_df['generation_rate'].fillna(method='ffill')  # Forward fill missing data
    
    return merged_df
