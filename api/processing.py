import pandas as pd

def process_energy_data(client_data: pd.DataFrame) -> pd.DataFrame:
    client_data['datetime'] = pd.to_datetime(client_data['datetime'])
    time_diff = client_data['datetime'].diff().dt.total_seconds().median()
    frequency = 12 if time_diff == 300 else 1
    num_columns = client_data.shape[1]
    kwh_column_idx, kw_column_idx = 7, 8

    if frequency == 12:
        if num_columns == 8:
            client_data.rename(columns={client_data.columns[kwh_column_idx]: 'kwh'}, inplace=True)
            client_data['kw'] = client_data['kwh'] * 12
        elif num_columns == 9:
            client_data.rename(columns={client_data.columns[kwh_column_idx]: 'kwh', client_data.columns[kw_column_idx]: 'kw'}, inplace=True)
    elif frequency == 1:
        if num_columns == 8:
            client_data['kw'] = client_data.iloc[:, kwh_column_idx]
            client_data.rename(columns={client_data.columns[kwh_column_idx]: 'kwh', 'kw': 'kw'}, inplace=True)
        elif num_columns == 9:
            client_data.rename(columns={client_data.columns[kwh_column_idx]: 'kwh', client_data.columns[kw_column_idx]: 'kw'}, inplace=True)
    return client_data

import pandas as pd

def generate_energy_summary(client_data, datetime_column='datetime', kwh_column='kwh', kw_column='kw'):
    # Ensure 'kwh' and 'kw' columns are numeric
    client_data[kwh_column] = pd.to_numeric(client_data[kwh_column], errors='coerce')
    client_data[kw_column] = pd.to_numeric(client_data[kw_column], errors='coerce')
    
    # Determine the frequency based on the time intervals in the datetime column
    client_data[datetime_column] = pd.to_datetime(client_data[datetime_column])  # Ensure datetime column is in proper format
    interval_seconds = client_data[datetime_column].diff().dt.total_seconds().median()
    frequency = 12 if interval_seconds == 300 else 1  # 12 for 5 minutes, 1 for 1 hour
    
    # Group by supply period and aggregate the necessary columns
    energy_summary = client_data.groupby("supply_period", sort=False).agg({
        kwh_column: "sum",
        kw_column: "max"
    }).reset_index()
    
    # Rename columns for readability
    energy_summary.rename(columns={kwh_column: 'kwh', kw_column: 'kw'}, inplace=True)
    
    # Calculate 'number of hours'
    energy_summary["number_of_hours"] = energy_summary["kwh"] / frequency
    
    # Add a total row with the sum of kWh and the max of kW
    total_row = {
        "supply_period": "Total",
        "kwh": energy_summary["kwh"].sum(),
        "kw": energy_summary["kw"].max(),
        "number_of_hours": energy_summary["number_of_hours"].sum()
    }
    energy_summary = pd.concat([energy_summary, pd.DataFrame([total_row])], ignore_index=True)
    
    # Calculate the load factor
    energy_summary["load_factor"] = (
        (energy_summary["kwh"] / (energy_summary['kw'] * energy_summary["number_of_hours"])) * 100
    )
    
    # Add Average, Max, Min rows (excluding the 'Total' row for calculations)
    stats_data = energy_summary.iloc[:-1]
    avg_row = stats_data.mean(numeric_only=True).to_dict()
    avg_row["supply_period"] = "Average"
    max_row = stats_data.max(numeric_only=True).to_dict()
    max_row["supply_period"] = "Max"
    min_row = stats_data.min(numeric_only=True).to_dict()
    min_row["supply_period"] = "Min"
    
    energy_summary = pd.concat([
        energy_summary,
        pd.DataFrame([avg_row, max_row, min_row])
    ], ignore_index=True)
    
    # Reorder columns
    energy_summary = energy_summary[["supply_period", "number_of_hours", "kwh", "kw", "load_factor"]]
    
    return energy_summary