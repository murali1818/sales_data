import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set the random seed for reproducibility
np.random.seed(42)

# Define at least 10 products
products = [
    {"Product_ID": 1, "Product_Name": "Floral Sundress", "Category": "Casual", "Retail Price": 40},
    {"Product_ID": 2, "Product_Name": "Evening Gown", "Category": "Formal", "Retail Price": 120},
    {"Product_ID": 3, "Product_Name": "Business Casual Dress", "Category": "Workwear", "Retail Price": 60},
    {"Product_ID": 4, "Product_Name": "Sequin Party Dress", "Category": "Party", "Retail Price": 80},
    {"Product_ID": 5, "Product_Name": "Summer Maxi Dress", "Category": "Seasonal", "Retail Price": 50},
    {"Product_ID": 6, "Product_Name": "Bridal Gown", "Category": "Wedding", "Retail Price": 200},
    {"Product_ID": 7, "Product_Name": "Traditional Ethnic Dress", "Category": "Ethnic", "Retail Price": 70},
    {"Product_ID": 8, "Product_Name": "Maternity Nursing Dress", "Category": "Maternity", "Retail Price": 45},
    {"Product_ID": 9, "Product_Name": "Sporty Athleisure Dress", "Category": "Athleisure", "Retail Price": 55},
    {"Product_ID": 10, "Product_Name": "Customizable Dress", "Category": "Customizable", "Retail Price": 65},
]

# Define date range
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 1, 31)
date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

# Generate random data
data = []
added_products_for_day = set()

for date in date_range:
    for product in products:
        # Check if the product is already added for the current day
        if product["Product_ID"] not in added_products_for_day:
            quantity = np.random.randint(10,30 )
            wholesale_price =round( 0.7 * product["Retail Price"])  # Random quantity between 5 and 50
            revenue = quantity * product["Retail Price"]
            profit=quantity*(product["Retail Price"]-wholesale_price)
            data.append({
                "Date": date.strftime("%d-%m-%Y"),
                "Product_ID": product["Product_ID"],
                "Product_Name": product["Product_Name"],
                "Category": product["Category"],
                "Quantity sold": quantity,
                "Wholesale_Price": wholesale_price,
                "Retail Price": product["Retail Price"],
                "Revenue": revenue,
                "profit":profit
            })

# Create a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv("dataset/sales_data(1).csv", index=False)
