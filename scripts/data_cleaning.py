import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))




import pandas as pd
from sqlalchemy import text
from database.db_connection import engine

# ----------------------------------
# Load data
# ----------------------------------
df = pd.read_sql("SELECT * FROM materials", engine)
print("Database connected successfully")

# ----------------------------------
# Data Cleaning
# ----------------------------------
df.fillna(0, inplace=True)

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
# Feature Engineering (MODULE 2 CORE)
# ----------------------------------

# 1️⃣ CO₂ Impact Index
df['co2_impact_index'] = df['co2_emission_kg'] * (
    1 - (df['recyclability_percent'] / 100)
)

# 2️⃣ Cost Efficiency Index
df['cost_efficiency_index'] = 1 / (df['cost_per_kg'] + 1)

# 3️⃣ Material Suitability Score
df['material_suitability_score'] = (
    (df['strength_score'] * 0.4) +
    (df['weight_capacity_kg'] * 0.3) +
    (df['cost_efficiency_index'] * 0.3)
)

# ----------------------------------
# OPTIONAL: Save engineered feature to DB
# (Do this ONLY if column exists)
# ----------------------------------
try:
    update_query = text("""
        UPDATE materials
        SET material_suitability_score = :score
        WHERE material_id = :id
    """)

    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(
                update_query,
                {"score": row['material_suitability_score'], "id": row['material_id']}
            )

    print("Engineered feature saved to database (optional step)")
except Exception:
    print("material_suitability_score not saved to DB (column not present)")

# ----------------------------------
# Validation Output (MANDATORY)
# ----------------------------------
print("\nFeature Engineering Completed Successfully\n")

print(df[
    [
        'material_name',
        'co2_impact_index',
        'cost_efficiency_index',
        'material_suitability_score'
    ]
].head())

print("\nSummary Statistics:")
print(df.describe())
