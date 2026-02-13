import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from database.db_connection import engine

# ----------------------------------
# Load data
# ----------------------------------
df = pd.read_sql("SELECT * FROM materials", engine)
print("Database connected successfully")

# ----------------------------------
# Data safety
# ----------------------------------
df.fillna(0, inplace=True)

# Ensure numeric
numeric_cols = [
    'strength_score',
    'weight_capacity_kg',
    'biodegradability_score',
    'recyclability_percent',
    'co2_emission_kg',
    'cost_per_kg'
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# ----------------------------------
# 🔥 RECOMPUTE MODULE-2 FEATURES 🔥
# ----------------------------------

# CO₂ Impact Index
df['co2_impact_index'] = df['co2_emission_kg'] * (
    1 - (df['recyclability_percent'] / 100)
)

# Cost Efficiency Index
df['cost_efficiency_index'] = 1 / (df['cost_per_kg'] + 1)

# Material Suitability Score
df['material_suitability_score'] = (
    (df['strength_score'] * 0.4) +
    (df['weight_capacity_kg'] * 0.3) +
    (df['cost_efficiency_index'] * 0.3)
)

# ----------------------------------
# Feature selection & targets
# ----------------------------------
X = df[
    [
        'strength_score',
        'weight_capacity_kg',
        'biodegradability_score',
        'recyclability_percent',
        'material_suitability_score'
    ]
]

y_cost = df['cost_per_kg']
y_co2 = df['co2_emission_kg']

# ----------------------------------
# Train-test split
# ----------------------------------
X_train, X_test, y_cost_train, y_cost_test = train_test_split(
    X, y_cost, test_size=0.2, random_state=42
)

_, _, y_co2_train, y_co2_test = train_test_split(
    X, y_co2, test_size=0.2, random_state=42
)

# ----------------------------------
# Scaling
# ----------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ----------------------------------
# Validation output
# ----------------------------------
print("\nML Dataset Prepared Successfully")
print(f"Training samples: {X_train_scaled.shape[0]}")
print(f"Testing samples: {X_test_scaled.shape[0]}")

print("\nSelected Features:")
print(X.columns.tolist())
