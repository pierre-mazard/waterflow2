import streamlit as st
import pandas as pd
import sqlalchemy
import os

# Connexion DB
DB_URL = os.getenv("DB_URL", "postgresql://postgres:postgres@localhost:5432/waterflow2")
engine = sqlalchemy.create_engine(DB_URL)

st.set_page_config(page_title="Waterflow 2 — Dashboard Expert", layout="wide")

st.title("🔬 Waterflow 2 — Dashboard Expert")
st.write("Plateforme d'analyse des prélèvements, prédictions et métriques du modèle.")

# ============================
# Chargement des données
# ============================


def load_measurements():
    query = """
        SELECT m.*, c.code_client
        FROM measurements m
        JOIN clients c ON m.id_client = c.id_client
        ORDER BY m.created_at DESC;
    """
    return pd.read_sql(query, engine)


def load_logs():
    query = "SELECT * FROM access_logs ORDER BY timestamp DESC;"
    return pd.read_sql(query, engine)

measurements = load_measurements()
logs = load_logs()

# ============================
# Filtres avancés
# ============================

st.sidebar.header("Filtres")

clients = measurements["code_client"].unique()
provenances = measurements["provenance"].unique()
predictions = measurements["prediction"].dropna().unique()

client_filter = st.sidebar.multiselect("Client", clients)
prov_filter = st.sidebar.multiselect("Provenance", provenances)
pred_filter = st.sidebar.multiselect("Prédiction", predictions)

filtered = measurements.copy()

if client_filter:
    filtered = filtered[filtered["code_client"].isin(client_filter)]

if prov_filter:
    filtered = filtered[filtered["provenance"].isin(prov_filter)]

if pred_filter:
    filtered = filtered[filtered["prediction"].isin(pred_filter)]

st.subheader("📊 Prélèvements filtrés")
st.dataframe(filtered, use_container_width=True)

# ============================
# Métriques du modèle
# ============================

st.subheader("📈 Métriques du modèle (exemple)")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Accuracy", "0.82")
col2.metric("Precision", "0.79")
col3.metric("Recall", "0.75")
col4.metric("F1-score", "0.77")

st.caption("Ces métriques seront remplacées par les métriques MLflow dans la phase MLOps.")

# ============================
# Logs RGPD
# ============================

st.subheader("📜 Journal des accès (RGPD)")
st.dataframe(logs, use_container_width=True)
