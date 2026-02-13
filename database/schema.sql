CREATE TABLE materials (
    material_id SERIAL PRIMARY KEY,
    material_type VARCHAR(100),
    strength INTEGER,
    weight_capacity FLOAT,
    biodegradability_score FLOAT,
    co2_emission FLOAT,
    recyclability_percent FLOAT,
    cost_per_unit FLOAT,
    product_category VARCHAR(100)
);
