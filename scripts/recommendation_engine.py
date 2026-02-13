import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import pandas as pd
from database.db_connection import engine
from ml_models.predict import predict_material

df = pd.read_sql("SELECT * FROM materials", engine)

df.fillna(0, inplace=True)

df['cost_efficiency_index'] = 1 / (df['cost_per_kg'] + 1)

df['material_suitability_score'] = (
    df['strength_score'] * 0.4 +
    df['weight_capacity_kg'] * 0.3 +
    df['cost_efficiency_index'] * 0.3
)

predicted_costs = []
predicted_co2 = []
final_scores = []

for _, row in df.iterrows():

    features = {
        'strength_score': row['strength_score'],
        'weight_capacity_kg': row['weight_capacity_kg'],
        'biodegradability_score': row['biodegradability_score'],
        'recyclability_percent': row['recyclability_percent'],
        'material_suitability_score': row['material_suitability_score']
    }

    cost, co2 = predict_material(features)

    predicted_costs.append(cost)
    predicted_co2.append(co2)

    score = (
        (1 / (cost + 1)) * 0.4 +
        (1 / (co2 + 1)) * 0.4 +
        row['material_suitability_score'] * 0.2
    )

    final_scores.append(score)

df['predicted_cost'] = predicted_costs
df['predicted_co2'] = predicted_co2
df['final_score'] = final_scores

ranked = df.sort_values(by='final_score', ascending=False)

print("\nTOP RECOMMENDED MATERIALS\n")

print(
    ranked[
        [
            'material_name',
            'predicted_cost',
            'predicted_co2',
            'final_score'
        ]
    ].head(5)
)
