

# Request model
class RequestData(BaseModel):
    client_name: str
    du_name: str
    start_date: date
    end_date: date
    discount_type: str
    floor_price: float
    du_discount: float

# Response model
#class ResponseData(BaseModel):
    #supply_period: str
    #kwh: str
    #generation_rate: float
    #DU Discounted Price: str
    #Total Charges: str
    #DU Rate Ave: str
    #DU Discounted Price Ave: str