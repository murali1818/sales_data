import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error

# Read data
df = pd.read_csv('sales_data/sales_data_advanced.csv', parse_dates=['Date'], dayfirst=True)

# Fill missing values
df_filled = df.fillna(0)

# Feature engineering
df_filled['Day_of_Week'] = df_filled['Date'].dt.dayofweek
df_filled['Month_of_Year'] = df_filled['Date'].dt.month

# Split data into features and target
X = df_filled.drop(['Quantity sold', 'Date'], axis=1)
y = df_filled['Quantity sold']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocess categorical features
X_train_encoded = pd.get_dummies(X_train, columns=['Product_Name', 'Product_ID'])
X_test_encoded = pd.get_dummies(X_test, columns=['Product_Name', 'Product_ID'])

# Ensure feature columns are consistent between training and testing datasets
missing_cols = set(X_train_encoded.columns) - set(X_test_encoded.columns)
for col in missing_cols:
    X_test_encoded[col] = 0

# Ensure all product IDs are present in both datasets
all_product_ids = set(X_train_encoded.filter(like='Product_ID').columns) | set(X_test_encoded.filter(like='Product_ID').columns)
for pid in all_product_ids:
    if pid not in X_train_encoded.columns:
        X_train_encoded[pid] = 0
    if pid not in X_test_encoded.columns:
        X_test_encoded[pid] = 0

# Initialize and train RandomForestRegressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train_encoded, y_train)

# Evaluate the model
y_pred = rf_model.predict(X_test_encoded)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error on the test set: {mse}")

# Cross-validation
cv_scores = cross_val_score(rf_model, X_train_encoded, y_train, cv=5)
print(f"Cross-Validation Scores: {cv_scores}")
print(f"Mean Cross-Validation Score: {cv_scores.mean()}")

# Predicting sales for the next one month
current_date = datetime.now().date()

product_ids = df_filled['Product_ID'].unique()
for product_id in product_ids:
    product_name = df_filled.loc[df_filled['Product_ID'] == product_id, 'Product_Name'].iloc[0]

    future_date = current_date + timedelta(days=30)
    future_date_features = pd.DataFrame({
        'Product_Name': [product_name],
        'Product_ID': [product_id],
        'Day_of_Week': [future_date.weekday()],
        'Month_of_Year': [future_date.month],
        'Temperature': [25.0],
        'Precipitation': [0.0],
        'Inflation': [2.5],
        'Holiday': [0],
        'Promotion_Active': [1],
        'GDP': [2000.0],
        'Campaign_Active': [0],
        'Special_Event': [0]
    })

    X_future = pd.get_dummies(future_date_features, columns=['Product_Name', 'Product_ID'])

    # Ensure feature columns are consistent with training dataset
    for col in set(X_train_encoded.columns) - set(X_future.columns):
        X_future[col] = 0

    forecasted_quantity = rf_model.predict(X_future)
    rounded_forecast = round(forecasted_quantity[0])

    print(f"Estimated sales of the ({product_id}){product_name} for the next one month: {rounded_forecast}")
