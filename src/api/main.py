from fastapi import FastAPI
from src.api.model_api import router as model_router
from src.api.data_api import router as data_router
from prometheus_fastapi_instrumentator import Instrumentator

from src.db.database import engine
from src.db.models import Base

app = FastAPI(
    title="Waterflow 2 API",
    version="1.0.0",
    description="API Model + Data pour Waterflow 2"
)

# Création automatique des tables
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

# Monitoring Prometheus
Instrumentator().instrument(app).expose(app)

# Routers
app.include_router(model_router, prefix="/api")
app.include_router(data_router, prefix="/api")

Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)

@app.get("/")
def root():
    return {"status": "API OK"}

