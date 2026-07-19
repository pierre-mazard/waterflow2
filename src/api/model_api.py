from fastapi import APIRouter
from pydantic import BaseModel
from src.ml.load_model import load_model

router = APIRouter()
model = load_model()

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

@router.post("/predict")
def predict(data: PredictionInput):
    """
    Endpoint de prédiction de potabilité.
    """
    features = [
        data.ph,
        data.hardness,
        data.solids,
        data.chloramines,
        data.sulfate,
        data.conductivity,
        data.organic_carbon,
        data.trihalomethanes,
        data.turbidity
    ]

    try:
        prediction = model.predict([features])[0]
        return {
            "prediction": int(prediction),
            "model_version": "v1",
            "status": "success"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
