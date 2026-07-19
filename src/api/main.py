from fastapi import FastAPI
from src.api.model_api import router as model_router
from src.api.data_api import router as data_router
from src.api.ocr_api import router as ocr_router

app = FastAPI(
    title="Waterflow 2 API",
    version="1.0.0",
    description="API Model + Data + OCR pour Waterflow 2"
)

app.include_router(model_router, prefix="/api")
app.include_router(data_router, prefix="/api")
app.include_router(ocr_router, prefix="/api")
