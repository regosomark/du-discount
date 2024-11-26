from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from calculator import calculate_discount
from utilss import (get_client_load_profile, get_generation_rate_data,)
from processing import process_energy_data, generate_energy_summary
from models import RequestData
import pandas as pd

app = FastAPI()

@app.get("/get_client_list")
async def get_client_list():
    """
    Fetches a list of clients and their respective supply periods.
    """
    # Simulate or fetch from database
    return [
        {
            "client_name": "digitaledge2",
            "supply_periods": ["2023-01-01 to 2023-12-31",
                                "2024-01-01 to 2024-12-31"]
        }
    ]

@app.post("/get_energy_and_rate_data")
async def get_energy_and_rate_data(request: RequestData):
    try:
        # Fetch and process client load profile
        client_data = get_client_load_profile(request.client_name, 
                                              request.start_date, 
                                              request.end_date)
        rate_data = get_generation_rate_data(request.du_name, 
                                             request.start_date,
                                             request.end_date)

        # Process the energy data
        processed_data = process_energy_data(client_data)
        energy_summary = generate_energy_summary(processed_data)

        # Merge with generation rate data
        result_df = combine_data(energy_summary, rate_data)

         # Calculate discounts using the unified function
        result = calculate_discount(
            result_df,
            floor_price=request.floor_price,
            du_discount=request.du_discount,
            discount_type=request.discount_type,
        )

        # Format the supply period and numeric values
        if not pd.api.types.is_datetime64_any_dtype(result['supply_period']):
            result['supply_period'] = pd.to_datetime(result['supply_period'], errors='coerce')

        formatted_result = [
            {
                "supply_period": row['supply_period'].strftime("%b-%Y") if pd.notnull(row['supply_period']) else None,
                "kwh": f"{float(row['kwh']):,.3f}" if pd.notnull(row['kwh']) else "0.000",
                "generation_rate": row['generation_rate'],
                "DU_Discounted_Price": row['DU Discounted Price'],
                "Total_Charges": f"{float(row['Total Charges']):,.2f}" if pd.notnull(row['Total Charges']) else "0.00",
                "DU_Rate_Ave": row['DU Rate Ave'],
                "DU_Discounted_Price_Ave": row['DU Discounted Price Ave'],
            }
            for _, row in result.iterrows()
        ]

        return formatted_result
    
    except Exception as e:
        raise HTTPException(status_code=500, 
                            detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")