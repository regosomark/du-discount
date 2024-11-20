from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from calculator import calculate_percentage_discount, calculate_fixed_discount
from utilss import get_client_load_profile, get_generation_rate_data, combine_data
from processing import process_energy_data, generate_energy_summary
import pandas as pd
from models import RequestData
app = FastAPI()

@app.get("/get_client_list")
async def get_client_list():

    # query to database
    
    return [
        {
            "client_name": "digitaledge2",
            "supply periods": [...]
        }
    ]

@app.post("/get_energy_and_rate_data")
async def get_energy_and_rate_data(request: RequestData):
    try:
        # Fetch and process client load profile
        client_data = get_client_load_profile(request.client_name, request.start_date, request.end_date)
        rate_data = get_generation_rate_data(request.du_name, request.start_date, request.end_date)
        
        # Process the energy data
        processed_data = process_energy_data(client_data)
        energy_summary = generate_energy_summary(processed_data)
        
        # Merge with generation rate data
        result_df = combine_data(energy_summary, rate_data)
        
        # Calculate discounts
        if request.discount_type == "Percentage":
            result = calculate_percentage_discount(result_df,request.floor_price, request.du_discount)
        elif request.discount_type == "Fixed":
            result = calculate_fixed_discount(result_df, request.floor_price, request.du_discount)
        else:
            raise ValueError("Invalid discount type. Choose 'Fixed' or 'Percentage'.")
        
        # Format the result for response
        final_result = result[[
            'supply_period', 'kwh', 'generation_rate', 'DU Discounted Price',
            'Total Charges', 'DU Rate Ave', 'DU Discounted Price Ave'
        ]].to_dict(orient="records")
        
        return final_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
