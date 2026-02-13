import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from database.db_connection import engine

df = pd.read_sql("SELECT * FROM materials", engine)

df.to_excel("sustainability_report.xlsx", index=False)

print("Sustainability Report Exported")
