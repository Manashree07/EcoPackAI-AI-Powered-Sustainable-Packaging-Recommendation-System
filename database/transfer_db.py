import pandas as pd
from sqlalchemy import create_engine

# LOCAL PostgreSQL
LOCAL_DB_URL = "postgresql://postgres:Shrutik1008@localhost:5432/ecopackai"

# RENDER PostgreSQL
RENDER_DB_URL = "postgresql://ecopackai_user:bMdZMZZ2MTIMtjU06T7KhD4a4IeQMfqt@dpg-d67eqncr85hc73blruqg-a.oregon-postgres.render.com/ecopackai_nufw"

# connect both databases
local_engine = create_engine(LOCAL_DB_URL)
render_engine = create_engine(RENDER_DB_URL)

print("Reading data from LOCAL PostgreSQL...")
df = pd.read_sql("SELECT * FROM materials", local_engine)

print("Uploading data to RENDER PostgreSQL...")
df.to_sql("materials", render_engine, if_exists="replace", index=False)

print("SUCCESS: Data transferred to Render PostgreSQL")
