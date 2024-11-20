import pandas as pd
from sqlalchemy import create_engine, text
from contextlib import contextmanager

DATABASE_URL = "postgresql://postgres:123456@localhost:5432/solx"

@contextmanager
def get_db_connection():
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()

def fetch_client_load_profile(client_name, start_date, end_date):
    query = text("""
        SELECT supply_period, datetime, date, correct_hour, hour, weekday, wesm, kwh
        FROM load_profiles."1hour_load_profile"
        WHERE client_id = (SELECT client_id FROM load_profiles.solx_clients WHERE client_name = :client_name)
        AND supply_period BETWEEN :start_date AND :end_date
    """)
    with get_db_connection() as connection:
        client_data = pd.read_sql(query, connection, params={
            "client_name": client_name,
            "start_date": start_date,
            "end_date": end_date
        })
    return client_data

def fetch_generation_rate_data(du_name, start_date, end_date):
    query = text("""
        SELECT supply_period, generation_rate
        FROM du_rates.generation_rate
        WHERE du_id = (SELECT du_id FROM du_rates.distribution_utilities WHERE du_name = :du_name)
        AND supply_period BETWEEN :start_date AND :end_date
    """)
    with get_db_connection() as connection:
        generation_rate_data = pd.read_sql(query, connection, params={
            "du_name": du_name,
            "start_date": start_date,
            "end_date": end_date
        })
    return generation_rate_data
