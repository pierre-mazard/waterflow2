from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.ml.load_model import load_model
from src.db.database import get_db
from src.db.models import Measurement, Client
import numpy as np
from datetime import datetime

router = APIRouter()

model, scaler, threshold = load_model()

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

def verify_api_key(api_key: str, db: Session):
    client = db.query(Client).filter(Client.api_key == api_key).first()
    if not client:
        raise HTTPException(status_code=401, detail="Clé API invalide")
    return client

@router.post("/predict_and_store")
def predict_and_store(data: PredictionInput, api_key: str = Header(None), db: Session = Depends(get_db)):
    if model is None or scaler is None or threshold is None:
        raise HTTPException(status_code=500, detail="Modèle non chargé")

    client = verify_api_key(api_key, db)

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
        data.interaction_turb_thm
    ]])

    features_scaled = scaler.transform(features)
    proba = float(model.predict_proba(features_scaled)[0][1])
    prediction = int(proba >= threshold)

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

    return {
        "status": "success",
        "probability": proba,
        "prediction": prediction,
        "threshold": float(threshold),
        "model_version": "xgboost_safe_v1",
        "measurement_id": measurement.id_measurement
    }