import pandas as pd

def process_energy_data(client_data: pd.DataFrame) -> pd.DataFrame:
    client_data['datetime'] = pd.to_datetime(client_data['datetime'])

    # Calculate the average frequency dynamically
    avg_points_per_hour = client_data.resample('h', on='datetime').count().hour.mean().round(0)

    kwh_column = 'kwh'
    kw_column = 'kw'

    # Dynamically calculate 'kw' based on the detected frequency
    if kwh_column in client_data.columns:
        if avg_points_per_hour > 0:  # Avoid division by zero or invalid cases
            frequency = 60 / (60 / avg_points_per_hour)
            client_data[kw_column] = client_data[kwh_column] * frequency
        else:
            client_data[kw_column] = client_data[kwh_column]  # Default case for no transformation

    return client_data


def generate_energy_summary(client_data, datetime_column='datetime', 
                            kwh_column='kwh', kw_column='kw'):
    # Ensure numeric columns
    client_data[kwh_column] = pd.to_numeric(client_data[kwh_column], errors='coerce').fillna(0)
    client_data[kw_column] = pd.to_numeric(client_data[kw_column], errors='coerce').fillna(0)
    client_data[datetime_column] = pd.to_datetime(client_data[datetime_column])
    
    # Group by supply period
    energy_summary = client_data.groupby("supply_period", sort=False).agg({
        kwh_column: "sum",
        kw_column: "max"
    }).reset_index()
    
    # Add total row
    total_row = {
        "supply_period": "Total",
        kwh_column: energy_summary[kwh_column].sum(),
        kw_column: energy_summary[kw_column].max()
    }
    energy_summary = pd.concat([energy_summary, pd.DataFrame([total_row])], ignore_index=True)
    
    # Add summary statistics (Average, Max, Min)
    stats_data = energy_summary.iloc[:-1]
    summary_stats = {
        "Average": stats_data.mean(numeric_only=True).to_dict(),
        "Max": stats_data.max(numeric_only=True).to_dict(),
        "Min": stats_data.min(numeric_only=True).to_dict()
    }
    for key, stat_row in summary_stats.items():
        stat_row["supply_period"] = key
        energy_summary = pd.concat([energy_summary, pd.DataFrame([stat_row])], ignore_index=True)
    
    return energy_summary
