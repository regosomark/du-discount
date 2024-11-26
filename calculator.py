import pandas as pd

def calculate_percentage_discount(merged_df: pd.DataFrame, floor_price: float, du_discount: float) -> pd.DataFrame:
    merged_df['generation_rate'] = pd.to_numeric(merged_df['generation_rate'], errors='coerce')
    merged_df['kwh'] = pd.to_numeric(merged_df['kwh'], errors='coerce').fillna(0)
    merged_df['DU Discounted Price'] = merged_df['generation_rate'] - (merged_df['generation_rate'] * (du_discount / 100))
    merged_df['DU Discounted Price'] = merged_df['DU Discounted Price'].clip(lower=floor_price).round(4)
    merged_df['DU Discounted Price'] = merged_df['DU Discounted Price'].apply(lambda x: f"{x:.4f}")
    merged_df['DU Discounted Price'] = pd.to_numeric(merged_df['DU Discounted Price'], errors='coerce')
    merged_df['Total Charges'] = merged_df['kwh'] * merged_df['DU Discounted Price']
    du_rate_ave = merged_df['generation_rate'].mean()
    merged_df['DU Rate Ave'] = f"{du_rate_ave:.4f}"
    discounted_price_ave = max(du_rate_ave - (du_rate_ave * (du_discount / 100)), floor_price)
    merged_df['DU Discounted Price Ave'] = f"{discounted_price_ave:.4f}"
    merged_df['kwh'] = merged_df['kwh'].apply(lambda x: f"{x:,.3f}")
    merged_df['Total Charges'] = merged_df['Total Charges'].apply(lambda x: f"{x:,.2f}")
    return merged_df

def calculate_fixed_discount(merged_df: pd.DataFrame, floor_price: float, du_discount: float) -> pd.DataFrame:
    merged_df['generation_rate'] = pd.to_numeric(merged_df['generation_rate'], errors='coerce')
    merged_df['kwh'] = pd.to_numeric(merged_df['kwh'], errors='coerce').fillna(0)
    merged_df['DU Discounted Price'] = merged_df['generation_rate'] - du_discount
    merged_df['DU Discounted Price'] = merged_df['DU Discounted Price'].clip(lower=floor_price).round(4)
    merged_df['DU Discounted Price'] = merged_df['DU Discounted Price'].apply(lambda x: f"{x:.4f}")
    merged_df['DU Discounted Price'] = pd.to_numeric(merged_df['DU Discounted Price'], errors='coerce')
    merged_df['Total Charges'] = merged_df['kwh'] * merged_df['DU Discounted Price']
    du_rate_ave = merged_df['generation_rate'].mean()
    merged_df['DU Rate Ave'] = f"{du_rate_ave:.4f}"
    discounted_price_ave = max(du_rate_ave - du_discount, floor_price)
    merged_df['DU Discounted Price Ave'] = f"{discounted_price_ave:.4f}"
    merged_df['kwh'] = merged_df['kwh'].apply(lambda x: f"{x:,.3f}")
    merged_df['Total Charges'] = merged_df['Total Charges'].apply(lambda x: f"{x:,.2f}")
    return merged_df


def calculate_discount(merged_df: pd.DataFrame, floor_price: float, du_discount: float, discount_type: str) -> pd.DataFrame:
    merged_df['generation_rate'] = pd.to_numeric(merged_df['generation_rate'], errors='coerce')
    merged_df['kwh'] = pd.to_numeric(merged_df['kwh'], errors='coerce').fillna(0)
    
    if discount_type == "Percentage":
        merged_df['DU Discounted Price'] = merged_df['generation_rate'] * (1 - du_discount / 100)
    elif discount_type == "Fixed":
        merged_df['DU Discounted Price'] = merged_df['generation_rate'] - du_discount
    else:
        raise ValueError("Invalid discount type. Choose 'Fixed' or 'Percentage'.")
    
    # Clip at floor price
    merged_df['DU Discounted Price'] = merged_df['DU Discounted Price'].clip(lower=floor_price).round(4)
    
    # Calculate total charges
    merged_df['Total Charges'] = merged_df['kwh'] * merged_df['DU Discounted Price']
    
    # Add summary statistics
    du_rate_ave = merged_df['generation_rate'].mean()
    merged_df['DU Rate Ave'] = f"{du_rate_ave:.4f}"
    discounted_price_ave = merged_df['DU Discounted Price'].mean()
    merged_df['DU Discounted Price Ave'] = f"{discounted_price_ave:.4f}"
    
    return merged_df
