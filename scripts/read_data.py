import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import pandas as pd
from database.db_connection import engine

material_df = pd.read_sql("SELECT * FROM materials", engine)
product_df = pd.read_sql("SELECT * FROM product", engine)

print(material_df.head())
print(product_df.head())

