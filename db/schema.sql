-- ============================================================
-- Waterflow 2 - Schéma SQL (PostgreSQL)
-- ============================================================

-- ===========================
-- Table : clients
-- ===========================
CREATE TABLE clients (
    id_client SERIAL PRIMARY KEY,
    code_client VARCHAR(50) UNIQUE NOT NULL,
    nom_structure VARCHAR(255) NOT NULL,
    adresse_postale TEXT,
    api_key VARCHAR(255) UNIQUE NOT NULL,
    date_creation TIMESTAMP DEFAULT NOW(),
    actif BOOLEAN DEFAULT TRUE
);

-- ===========================
-- Table : measurements
-- ===========================
CREATE TABLE measurements (
    id_measurement SERIAL PRIMARY KEY,
    id_client INTEGER NOT NULL REFERENCES clients(id_client) ON DELETE CASCADE,
    date_prelevement TIMESTAMP NOT NULL,
    lieu_prelevement VARCHAR(255),

    -- Mesures physico-chimiques
    ph NUMERIC,
    hardness NUMERIC,
    solids NUMERIC,
    chloramines NUMERIC,
    sulfate NUMERIC,
    conductivity NUMERIC,
    organic_carbon NUMERIC,
    trihalomethanes NUMERIC,
    turbidity NUMERIC,

    provenance VARCHAR(20) CHECK (provenance IN ('Saisie', 'OCR')),
    prediction INTEGER,
    prediction_model_version VARCHAR(50),

    created_at TIMESTAMP DEFAULT NOW()
);

-- ===========================
-- Table : access_logs
-- ===========================
CREATE TABLE access_logs (
    id_log SERIAL PRIMARY KEY,
    api_key VARCHAR(255) NOT NULL,
    endpoint VARCHAR(255) NOT NULL,
    status_code INTEGER NOT NULL,
    duration_ms INTEGER,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Indexes pour performance
CREATE INDEX idx_measurements_client ON measurements(id_client);
CREATE INDEX idx_logs_api_key ON access_logs(api_key);
CREATE INDEX idx_logs_timestamp ON access_logs(timestamp);
