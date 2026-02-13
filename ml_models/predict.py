import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import joblib
import pandas as pd

# Load models
cost_model = joblib.load("ml_models/cost_model.pkl")
co2_model = joblib.load("ml_models/co2_model.pkl")

def predict_material(features_dict):

    df = pd.DataFrame([features_dict])

    predicted_cost = cost_model.predict(df)[0]
    predicted_co2 = co2_model.predict(df)[0]

    return predicted_cost, predicted_co2
