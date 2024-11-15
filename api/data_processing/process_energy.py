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

def generate_energy_summary(client_data: pd.DataFrame, datetime_column: str = 'datetime', kwh_column: str = 'kwh', kw_column: str = 'kw') -> pd.DataFrame:
    # Ensure 'kwh' and 'kw' columns are numeric
    client_data[kwh_column] = pd.to_numeric(client_data[kwh_column], errors='coerce')
    client_data[kw_column] = pd.to_numeric(client_data[kw_column], errors='coerce')

    # Determine the frequency based on the time intervals in the datetime column
    interval_seconds = client_data[datetime_column].diff().dt.total_seconds().median()
    frequency = 12 if interval_seconds == 300 else 1  # 12 for 5 minutes, 1 for 1 hour

    # Group by supply period and aggregate the necessary columns
    energy_summary = client_data.groupby("supply_period", sort=False).agg({
        "supply_period": "count",
        kwh_column: "sum",
        kw_column: "max"
    })

    # Rename columns for readability
    energy_summary.columns = ["number of intervals", "kwh", "kw"]

    # Calculate 'number of hours' based on frequency and drop 'number of intervals'
    energy_summary["number of hours"] = energy_summary["number of intervals"] / frequency
    energy_summary.drop(columns=["number of intervals"], inplace=True)

    # Add a total row with the sum of kWh and the max of kW
    energy_summary.loc["Total"] = energy_summary.sum(numeric_only=True)
    energy_summary.loc["Total", "kw"] = energy_summary.iloc[:-1]["kw"].max()

    # Calculate the load factor
    energy_summary["load factor"] = (energy_summary["kwh"] / (energy_summary['kw'] * energy_summary["number of hours"])) * 100

    # Create a copy of the summary client_data without the Total row for statistics
    original_energy_summary = energy_summary.iloc[:-1].copy()

    # Add Average, Max, Min rows based on the original client_data (excluding 'Total')
    energy_summary.loc["Average"] = original_energy_summary.mean(numeric_only=True)
    energy_summary.loc["Max"] = original_energy_summary.max(numeric_only=True)
    energy_summary.loc["Min"] = original_energy_summary.min(numeric_only=True)

    # Reset index to remove 'supply_period' from being the index
    energy_summary = energy_summary.reset_index()

    # Reorder columns as specified
    energy_summary = energy_summary[["supply_period", "number of hours", "kwh", "kw", "load factor"]]

    return energy_summary
