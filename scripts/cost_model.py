import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))



import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from database.db_connection import engine

df = pd.read_sql("SELECT * FROM materials", engine)
print("Database connected successfully")

X = df[['strength_score', 'weight_capacity_kg', 'material_suitability_score']]
y = df['cost_per_kg']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

print("Cost Prediction Model Trained")
print("MAE:", mae)
print("RMSE:", rmse)
print("R2 Score:", r2)
