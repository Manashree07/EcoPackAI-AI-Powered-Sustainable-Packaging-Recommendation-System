import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from database.db_connection import engine

# ----------------------------------
# Load data
# ----------------------------------
df = pd.read_sql("SELECT * FROM materials", engine)
print("Database connected successfully")

# ----------------------------------
# Safety check
# ----------------------------------
df.fillna(0, inplace=True)

# ----------------------------------
# Recompute engineered feature (BEST PRACTICE)
# ----------------------------------
df['cost_efficiency_index'] = 1 / (df['cost_per_kg'] + 1)

df['material_suitability_score'] = (
    (df['strength_score'] * 0.4) +
    (df['weight_capacity_kg'] * 0.3) +
    (df['cost_efficiency_index'] * 0.3)
)

# ----------------------------------
# Feature & Target selection
# ----------------------------------
X = df[
    [
        'strength_score',
        'weight_capacity_kg',
        'material_suitability_score'
    ]
]

y = df['co2_emission_kg']

# ----------------------------------
# Train-test split
# ----------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ----------------------------------
# Train XGBoost model
# ----------------------------------
model = XGBRegressor(random_state=42)
model.fit(X_train, y_train)

# ----------------------------------
# Prediction & Evaluation
# ----------------------------------
predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

# ----------------------------------
# Output (MANDATORY FOR MODULE 4)
# ----------------------------------
print("\nCO₂ Prediction Model Trained")
print("MAE:", mae)
print("RMSE:", rmse)
print("R2 Score:", r2)
