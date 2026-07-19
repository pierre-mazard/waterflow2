# Modèle de Données — Waterflow 2 (MCD & MPD)

## 1. Objectifs du modèle de données

Le modèle de données Waterflow 2 doit permettre :

- la gestion des clients (ID, nom, adresse, clé API),
- le dépôt de prélèvements (mesures physico-chimiques),
- l’ingestion OCR (provenance : Saisie / OCR),
- la prédiction de potabilité,
- la journalisation des accès (RGPD),
- la traçabilité des actions (client, analyste, responsable).

---

# 2. MCD (Modèle Conceptuel de Données)

### Entité : CLIENT
- id_client (Identifiant technique)
- code_client (Identifiant lisible, ex : CLIENT-042)
- nom_structure
- adresse_postale
- api_key (clé API unique)
- date_creation
- actif (bool)

### Entité : MEASUREMENT (Prélèvement)
- id_measurement
- id_client (FK → CLIENT)
- date_prelevement
- lieu_prelevement
- ph
- hardness
- solids
- chloramines
- sulfate
- conductivity
- organic_carbon
- trihalomethanes
- turbidity
- provenance (Saisie / OCR)
- prediction (0/1)
- prediction_model_version
- created_at

### Entité : ACCESS_LOG (Journal RGPD)
- id_log
- api_key
- endpoint
- status_code
- duration_ms
- timestamp

---

# 3. Associations

### CLIENT — MEASUREMENT
- Un client peut avoir plusieurs prélèvements.
- Un prélèvement appartient à un seul client.

Cardinalité :
CLIENT (1,n) —— (1,1) MEASUREMENT


### CLIENT — ACCESS_LOG
- Une clé API peut générer plusieurs logs.
- Un log appartient à une seule clé API.

Cardinalité :
CLIENT (1,n) —— (1,1) ACCESS_LOG


---

# 4. MPD (Modèle Physique de Données — PostgreSQL)

## Table : clients

```sql
CREATE TABLE clients (
    id_client SERIAL PRIMARY KEY,
    code_client VARCHAR(50) UNIQUE NOT NULL,
    nom_structure VARCHAR(255) NOT NULL,
    adresse_postale TEXT,
    api_key VARCHAR(255) UNIQUE NOT NULL,
    date_creation TIMESTAMP DEFAULT NOW(),
    actif BOOLEAN DEFAULT TRUE
);
```

## Tablle : measurements

```sql
CREATE TABLE measurements (
    id_measurement SERIAL PRIMARY KEY,
    id_client INTEGER REFERENCES clients(id_client),
    date_prelevement TIMESTAMP NOT NULL,
    lieu_prelevement VARCHAR(255),
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
```

## Table : access_log
```sql
CREATE TABLE access_logs (
    id_log SERIAL PRIMARY KEY,
    api_key VARCHAR(255) NOT NULL,
    endpoint VARCHAR(255) NOT NULL,
    status_code INTEGER NOT NULL,
    duration_ms INTEGER,
    timestamp TIMESTAMP DEFAULT NOW()
);
```

# 5. Contraintes RGPD

- La clé API identifie un client mais ne contient aucune donnée personnelle.

- Les journaux d’accès sont conservés pour la traçabilité (durée à définir dans docs/rgpd_note.md).

- Les données personnelles minimales sont :

    - nom de la structure,

    - adresse postale,

    - historique d’accès (via api_key).

# 6.Conclusion 

Ce modèle respecte :

- les exigences Waterflow 2 (API Data + Model + OCR),

- les user stories (client, analyste, responsable),

- les contraintes RGPD (journalisation, minimisation),

- les critères RNCP (C4, C14, C15).

Il servira de base :

- aux scripts SQL (db/schema.sql),

- à l’ORM (SQLAlchemy),

- à l’API Data,

- à l’interface expert,

- au monitoring.