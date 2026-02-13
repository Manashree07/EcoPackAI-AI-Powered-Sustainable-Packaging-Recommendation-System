import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import pandas as pd
import matplotlib.pyplot as plt
from database.db_connection import engine

df = pd.read_sql("SELECT * FROM materials", engine)

plt.figure()
plt.bar(df['material_name'], df['co2_emission_kg'])
plt.xticks(rotation=45)
plt.title("CO₂ Emissions by Material")
plt.tight_layout()
plt.show()
