from calculator import calculate_fixed_discount, calculate_percentage_discount
from datetime import date
from pydantic import BaseModel

def DuDiscount(data, discount_type, floor_price, du_discount):
    if discount_type == "Percentage":
        return calculate_percentage_discount(data, floor_price, du_discount)
    elif discount_type == "Fixed":
        return calculate_fixed_discount(data, floor_price, du_discount)
    else:
        raise ValueError("Invalid discount type. Choose 'Fixed' or 'Percentage'.")

# Request model
class RequestData(BaseModel):
    client_name: str
    du_name: str
    start_date: date
    end_date: date
    discount_type: str
    floor_price: float
    du_discount: float

class DuDiscount(BaseModel):
    floor_price: float = Field(..., ge=0)  # Non-negative floor price
    du_discount: float = Field(..., ge=0)   # Non-negative discount
    du_name: str #changed from du_id to du_name
    du_discount_type: str  # Add this line to include discount type

# Response model
#class ResponseData(BaseModel):
    #supply_period: str
    #kwh: str
    #generation_rate: float
    #DU Discounted Price: str
    #Total Charges: str
    #DU Rate Ave: str
    #DU Discounted Price Ave: str
