from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from calculator import calculate_percentage_discount, calculate_fixed_discount
from utilss import get_energy_summary, get_generation_rate_data
from processing import process_energy_data, generate_energy_summary
import pandas as pd

app = FastAPI()

class RequestData(BaseModel):
    client_name: str
    du_name: str
    start_date: str
    end_date: str
    discount_type: str
    floor_price: float
    du_discount: float

@app.post("/get_energy_and_rate_data")
async def get_energy_and_rate_data(request: RequestData):
    try:
        # Fetch energy summary and generation rate data
        energy_summary = get_energy_summary(request.client_name, request.start_date, request.end_date)
        generation_rate_data = get_generation_rate_data(request.du_name, request.start_date, request.end_date)
        
        # Process energy data
        client_data = process_energy_data(energy_summary)
        
        # Merge dataframes on 'supply_period'
        merged_df = pd.merge(client_data, generation_rate_data, on="supply_period", how="left")
        
        # Calculate discounts
        if request.discount_type == "Percentage":
            final_result = calculate_percentage_discount(merged_df, request.floor_price, request.du_discount)
        elif request.discount_type == "Fixed":
            final_result = calculate_fixed_discount(merged_df, request.floor_price, request.du_discount)
        else:
            raise ValueError("Invalid discount type. Choose 'Fixed' or 'Percentage'.")

        # Return the relevant data
        result = final_result[['supply_period', 'kwh', 'generation_rate', 'DU Discounted Price', 'Total Charges', 'DU Rate Ave', 'DU Discounted Price Ave']].to_dict(orient="records")
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
