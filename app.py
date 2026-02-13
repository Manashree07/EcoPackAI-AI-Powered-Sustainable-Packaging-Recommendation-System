import sys
import os

# Ensure project root is in path
sys.path.append(os.path.dirname(__file__))

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

from database.db_connection import engine
from ml_models.predict import predict_material

from flask import render_template

import plotly.express as px
from flask import render_template



app = Flask(__name__)
CORS(app)

# ----------------------------------
# Home route
# ----------------------------------



@app.route("/ui")
def ui():
    return render_template("index.html")



@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "message": "EcoPackAI API is running"
    })


# ----------------------------------
# Get all materials
# ----------------------------------
@app.route("/materials", methods=["GET"])
def get_materials():

    try:
        df = pd.read_sql("SELECT * FROM materials", engine)

        return jsonify({
            "status": "success",
            "count": len(df),
            "data": df.to_dict(orient="records")
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ----------------------------------
# AI Recommendation API
# ----------------------------------
@app.route("/recommend", methods=["GET", "POST"])
def recommend():

    # Handle GET request (browser test)
    if request.method == "GET":
        return jsonify({
            "status": "info",
            "message": "Use POST request with JSON body to get recommendations"
        })

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON data provided"
            }), 400

        strength = float(data.get("strength_score", 0))
        weight = float(data.get("weight_capacity_kg", 0))
        biodegradability = float(data.get("biodegradability_score", 0))
        recyclability = float(data.get("recyclability_percent", 0))

        # Feature engineering
        cost_efficiency = 1 / (1 + 1)

        suitability = (
            strength * 0.4 +
            weight * 0.3 +
            cost_efficiency * 0.3
        )

        features = {
            "strength_score": strength,
            "weight_capacity_kg": weight,
            "biodegradability_score": biodegradability,
            "recyclability_percent": recyclability,
            "material_suitability_score": suitability
        }

        predicted_cost, predicted_co2 = predict_material(features)

        return jsonify({
            "status": "success",
            "predicted_cost": float(predicted_cost),
            "predicted_co2": float(predicted_co2),
            "suitability_score": float(suitability)
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ----------------------------------
# Rank all materials
# ----------------------------------
@app.route("/rank-materials", methods=["GET"])
def rank_materials():

    try:

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
                "strength_score": row['strength_score'],
                "weight_capacity_kg": row['weight_capacity_kg'],
                "biodegradability_score": row['biodegradability_score'],
                "recyclability_percent": row['recyclability_percent'],
                "material_suitability_score": row['material_suitability_score']
            }

            cost, co2 = predict_material(features)

            predicted_costs.append(float(cost))
            predicted_co2.append(float(co2))

            score = (
                (1 / (cost + 1)) * 0.4 +
                (1 / (co2 + 1)) * 0.4 +
                row['material_suitability_score'] * 0.2
            )

            final_scores.append(float(score))

        df['predicted_cost'] = predicted_costs
        df['predicted_co2'] = predicted_co2
        df['final_score'] = final_scores

        ranked = df.sort_values(by="final_score", ascending=False)

        return jsonify({
            "status": "success",
            "count": len(ranked),
            "data": ranked.to_dict(orient="records")
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ----------------------------------
# Run server
# ----------------------------------
if __name__ == "__main__":

    print("Starting EcoPackAI Flask Server...")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )




@app.route("/dashboard")
def dashboard():

    df = pd.read_sql("SELECT * FROM materials", engine)

    # CO2 chart
    co2_chart = px.bar(
        df,
        x="material_name",
        y="co2_emission_kg",
        title="CO₂ Emissions by Material",
        color="co2_emission_kg"
    )

    co2_graph = co2_chart.to_html(full_html=False)

    # Cost chart
    cost_chart = px.bar(
        df,
        x="material_name",
        y="cost_per_kg",
        title="Cost per Material",
        color="cost_per_kg"
    )

    cost_graph = cost_chart.to_html(full_html=False)

    return render_template(
        "dashboard.html",
        co2_graph=co2_graph,
        cost_graph=cost_graph
    )
