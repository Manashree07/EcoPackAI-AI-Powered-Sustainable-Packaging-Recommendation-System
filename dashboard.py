import pandas as pd
import plotly.express as px
from database.db_connection import engine

df = pd.read_sql("SELECT * FROM materials", engine)

fig = px.bar(df, x="material_name", y="co2_emission_kg",
             title="CO₂ Emission Comparison")

fig.show()
