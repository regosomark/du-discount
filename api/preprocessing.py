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