import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import pandas as pd
import joblib
from database.db_connection import engine
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

# Load data
df = pd.read_sql("SELECT * FROM materials", engine)

# Feature engineering
df.fillna(0, inplace=True)

df['cost_efficiency_index'] = 1 / (df['cost_per_kg'] + 1)

df['material_suitability_score'] = (
    df['strength_score'] * 0.4 +
    df['weight_capacity_kg'] * 0.3 +
    df['cost_efficiency_index'] * 0.3
)

features = [
    'strength_score',
    'weight_capacity_kg',
    'biodegradability_score',
    'recyclability_percent',
    'material_suitability_score'
]

X = df[features]

# Targets
y_cost = df['cost_per_kg']
y_co2 = df['co2_emission_kg']

# Train models
cost_model = RandomForestRegressor()
co2_model = XGBRegressor()

cost_model.fit(X, y_cost)
co2_model.fit(X, y_co2)

# Save models
joblib.dump(cost_model, "ml_models/cost_model.pkl")
joblib.dump(co2_model, "ml_models/co2_model.pkl")

print("Models saved successfully")
