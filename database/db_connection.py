import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("postgresql://postgres:Shrutik1008@localhost:5432/ecopackai")

# Fix postgres:// issue
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"}
)

print("Database connected successfully")

