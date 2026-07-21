CREATE TABLE clients (
    id_client SERIAL PRIMARY KEY,
    code_client VARCHAR(50) UNIQUE NOT NULL,
    nom_structure VARCHAR(255) NOT NULL,
    adresse_postale TEXT,
    api_key VARCHAR(255) UNIQUE NOT NULL,
    date_creation TIMESTAMP,
    actif BOOLEAN DEFAULT TRUE
);

CREATE TABLE measurements (
    id_measurement SERIAL PRIMARY KEY,
    id_client INTEGER REFERENCES clients(id_client),
    date_prelevement TIMESTAMP NOT NULL,
    lieu_prelevement VARCHAR(255),
    ph FLOAT,
    hardness FLOAT,
    solids FLOAT,
    chloramines FLOAT,
    sulfate FLOAT,
    conductivity FLOAT,
    organic_carbon FLOAT,
    trihalomethanes FLOAT,
    turbidity FLOAT,
    provenance VARCHAR(20),
    prediction INTEGER,
    prediction_model_version VARCHAR(50),
    created_at TIMESTAMP
);

CREATE TABLE access_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    endpoint TEXT,
    api_key TEXT
);
