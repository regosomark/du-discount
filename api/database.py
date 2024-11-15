import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

# Replace with your actual database connection string
DATABASE_URL = "postgresql://postgres:123456@localhost:5432/solx"

# Database connection setup
def get_db_connection():
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    return connection

# Fetch energy summary from the database
def fetch_energy_summary(client_name, start_date, end_date):
    connection = get_db_connection()
    query = f"""
        SELECT supply_period, datetime, date, correct_hour, hour, weekday, wesm, kwh
        FROM load_profiles."1hour_load_profile"
        WHERE client_id = (SELECT client_id FROM load_profiles.solx_clients WHERE client_name = '{client_name}')
        AND supply_period BETWEEN '{start_date}' AND '{end_date}'
    """
    client_data = pd.read_sql(query, connection)
    connection.close()
    return client_data

# Fetch generation rate data from the database
def fetch_generation_rate_data(du_name, start_date, end_date):
    connection = get_db_connection()
    query = f"""
        SELECT supply_period, generation_rate
        FROM du_rates.generation_rate
        WHERE du_id = (SELECT du_id FROM du_rates.distribution_utilities WHERE du_name = '{du_name}')
        AND supply_period BETWEEN '{start_date}' AND '{end_date}'
    """
    generation_rate_data = pd.read_sql(query, connection)
    connection.close()
    return generation_rate_data
