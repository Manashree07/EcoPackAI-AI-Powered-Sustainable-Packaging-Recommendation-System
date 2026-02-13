import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from database.db_connection import engine

df = pd.read_sql("SELECT * FROM product", engine)

priority_map = {'High': 3, 'Medium': 2, 'Low': 1}
df['sustainability_priority'] = df['sustainability_priority'].map(priority_map)

df.to_csv("cleaned_product.csv", index=False)

print("Product data cleaned")
