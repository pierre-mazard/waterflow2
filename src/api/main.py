from fastapi import FastAPI
from src.api.model_api import router as model_router

app = FastAPI(
    title="Waterflow 2 API",
    version="1.0.0",
    description="API Model pour la prédiction de potabilité"
)

app.include_router(model_router, prefix="/api")
