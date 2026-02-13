from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:Shrutik1008@localhost:5432/ecopackai"
)

print("Database connected successfully")







