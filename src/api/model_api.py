from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.ml.load_model import load_model
from src.db.database import get_db
from src.db.models import Measurement, Client
import numpy as np
from datetime import datetime

router = APIRouter()

# ⚠️ Chargement dynamique du modèle calibré
model = None
scaler = None
threshold = None

def ensure_model_loaded():
    global model, scaler, threshold
    if model is None or scaler is None or threshold is None:
        model, scaler, threshold = load_model()
    if model is None or scaler is None or threshold is None:
        raise HTTPException(status_code=500, detail="Modèle non chargé")

# ---------------------------
# Schéma d'entrée (12 features brutes)
# ---------------------------

class PredictionInput(BaseModel):
    ph: float
    hardness: float
    solids: float
    chloramines: float
    sulfate: float
    conductivity: float
    organic_carbon: float
    trihalomethanes: float
    turbidity: float
    interaction_tds_cond: float
    interaction_ph_carbon: float
    interaction_turb_thm: float

# ---------------------------
# Vérification clé API
# ---------------------------

def verify_api_key(api_key: str, db: Session):
    client = db.query(Client).filter(Client.api_key == api_key).first()
    if not client:
        raise HTTPException(status_code=401, detail="Clé API invalide")
    return client

# ---------------------------
# Endpoint principal
# ---------------------------

@router.post("/predict_and_store")
def predict_and_store(
    data: PredictionInput,
    api_key: str = Header(None),
    db: Session = Depends(get_db)
):
    ensure_model_loaded()
    client = verify_api_key(api_key, db)

    # ---------------------------
    # Recalcul des features OMS/EPA (exactement comme dans train.py)
    # ---------------------------
    risk_chloramines = int(data.chloramines > 4)
    risk_thm = int(data.trihalomethanes > 80)
    risk_turbidity = int(data.turbidity > 5)
    risk_ph = int((data.ph < 6.5) or (data.ph > 8.5))
    risk_tds = int(data.solids > 1000)
    risk_sulfate = int(data.sulfate > 250)
    risk_conductivity = int(data.conductivity > 800)

    # ---------------------------
    # Construction du vecteur complet (19 features)
    # ⚠️ Ordre IDENTIQUE à train.py
    # ---------------------------
    features = np.array([[
        data.ph,
        data.hardness,
        data.solids,
        data.chloramines,
        data.sulfate,
        data.conductivity,
        data.organic_carbon,
        data.trihalomethanes,
        data.turbidity,
        data.interaction_tds_cond,
        data.interaction_ph_carbon,
        data.interaction_turb_thm,
        risk_chloramines,
        risk_thm,
        risk_turbidity,
        risk_ph,
        risk_tds,
        risk_sulfate,
        risk_conductivity
    ]])

    # ---------------------------
    # Scaling + prédiction
    # ---------------------------
    features_scaled = scaler.transform(features)
    proba = float(model.predict_proba(features_scaled)[0][1])
    prediction = int(proba >= threshold)

    # ---------------------------
    # Analyse des risques (OMS/EPA)
    # ---------------------------
    risks = []
    if risk_chloramines: risks.append("chloramines au-dessus du seuil OMS (4 mg/L)")
    if risk_thm: risks.append("trihalométhanes au-dessus du seuil OMS (80 µg/L)")
    if risk_turbidity: risks.append("turbidité élevée (> 5 NTU)")
    if risk_ph: risks.append("pH hors plage recommandée (6.5–8.5)")
    if risk_tds: risks.append("TDS très élevés (> 1000 mg/L)")
    if risk_sulfate: risks.append("sulfates élevés (> 250 mg/L)")
    if risk_conductivity: risks.append("conductivité élevée (> 800 µS/cm)")

    risk_origin = "aucun paramètre hors seuil OMS/EPA" if len(risks) == 0 else ", ".join(risks)

    # ---------------------------
    # Enregistrement en base
    # ---------------------------
    measurement = Measurement(
        id_client=client.id_client,
        date_prelevement=datetime.now(),
        lieu_prelevement="API",
        ph=data.ph,
        hardness=data.hardness,
        solids=data.solids,
        chloramines=data.chloramines,
        sulfate=data.sulfate,
        conductivity=data.conductivity,
        organic_carbon=data.organic_carbon,
        trihalomethanes=data.trihalomethanes,
        turbidity=data.turbidity,
        provenance="API",
        prediction=prediction,
        prediction_model_version="xgboost_safe_v1",
        created_at=datetime.now()
    )

    db.add(measurement)
    db.commit()
    db.refresh(measurement)

    # ---------------------------
    # Réponse API enrichie
    # ---------------------------
    return {
        "status": "success",
        "probability": proba,
        "prediction": prediction,
        "threshold": float(threshold),
        "potability_label": (
            "potable (haut niveau de confiance)" if proba >= threshold and len(risks) == 0
            else "potable" if proba >= 0.5 and len(risks) == 0
            else "potable mais avec risque" if proba >= 0.3 and len(risks) == 0
            else "non potable"
        ),
        "risk_origin": risk_origin,
        "model_version": "xgboost_safe_v1",
        "measurement_id": measurement.id_measurement
    }
