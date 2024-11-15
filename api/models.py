from calculator import calculate_percentage_discount, calculate_fixed_discount

def DuDiscount(data, discount_type, floor_price, du_discount):
    if discount_type == "Percentage":
        return calculate_percentage_discount(data, floor_price, du_discount)
    elif discount_type == "Fixed":
        return calculate_fixed_discount(data, floor_price, du_discount)
    else:
        raise ValueError("Invalid discount type. Choose 'Fixed' or 'Percentage'.")
