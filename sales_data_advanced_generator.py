import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Define product names
product_names = [
    'Floral Sundress', 'Evening Gown', 'Business Casual Dress', 'Sequin Party Dress', 'Summer Maxi Dress',
    'Bridal Gown', 'Traditional Ethnic Dress', 'Maternity Nursing Dress', 'Sporty Athleisure Dress',
    'Customizable Dress'
]

# Generate product IDs
product_ids = list(range(1, len(product_names) + 1))

# Create a dictionary to map product names to product IDs
product_id_mapping = dict(zip(product_names, product_ids))

# Generate sales data for each product for every day
date_rng = pd.date_range(start='2023-01-01', end='2024-01-30', freq='D')
sales_data = pd.DataFrame(columns=['Date', 'Product_ID', 'Product_Name', 'Quantity sold'])

for product in product_names:
    product_id = product_id_mapping[product]
    sales_data_product = pd.DataFrame({'Date': date_rng, 'Product_ID': product_id, 'Product_Name': product, 'Quantity sold': np.random.randint(10, 100, size=(len(date_rng)))})
    sales_data = pd.concat([sales_data, sales_data_product], ignore_index=True, sort=False)

# Generate economic indicators data
economic_data = pd.DataFrame(date_rng, columns=['Date'])
economic_data['GDP'] = np.random.uniform(1000, 2000, size=(len(date_rng)))
economic_data['Inflation'] = np.random.uniform(1, 5, size=(len(date_rng)))

# Generate marketing campaigns and promotions data
marketing_data = pd.DataFrame(date_rng, columns=['Date'])
marketing_data['Campaign_Active'] = np.random.choice([0, 1], size=(len(date_rng)))
marketing_data['Promotion_Active'] = np.random.choice([0, 1], size=(len(date_rng)))

# Generate a list of common holidays
common_holidays = pd.DataFrame({
    'Date': pd.to_datetime(['2023-01-01', '2023-12-25', '2024-01-01', '2024-07-04']),
    'Holiday': [1, 1, 1, 1],
    'Special_Event': [0, 0, 0, 1]
})

# Generate weather data
weather_data = pd.DataFrame(date_rng, columns=['Date'])
weather_data['Temperature'] = np.random.uniform(50, 90, size=(len(date_rng)))
weather_data['Precipitation'] = np.random.uniform(0, 1, size=(len(date_rng)))

# Merge all generated datasets
df_sales = pd.merge(sales_data, economic_data, on='Date', how='left')
df_sales = pd.merge(df_sales, marketing_data, on='Date', how='left')
df_sales = pd.merge(df_sales, common_holidays, on='Date', how='left')
df_sales = pd.merge(df_sales, weather_data, on='Date', how='left')

# Sort the DataFrame by date and product ID
df_sales = df_sales.sort_values(by=['Date', 'Product_ID'])

# Save the generated dataset to a CSV file
df_sales.to_csv('sales_data/sales_data_advanced1.csv', index=False)
