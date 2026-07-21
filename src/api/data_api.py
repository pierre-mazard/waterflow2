from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from src.db.database import get_db
from src.db.models import Client, Measurement
from pydantic import BaseModel

router = APIRouter()

# ---------------------------
# Schémas Pydantic
# ---------------------------

class ClientCreate(BaseModel):
    code_client: str
    nom_structure: str
    adresse_postale: str

class MeasurementCreate(BaseModel):
    ph: float
    hardness: float
    solids: float
    chloramines: float
    sulfate: float
    conductivity: float
    organic_carbon: float
    trihalomethanes: float
    turbidity: float

# ---------------------------
# Vérification clé API client
# ---------------------------

def verify_api_key(api_key: str, db: Session):
    client = db.query(Client).filter(Client.api_key == api_key).first()
    if not client:
        raise HTTPException(status_code=401, detail="Clé API invalide")
    return client

# ---------------------------
# Création client (admin)
# ---------------------------

@router.post("/clients")
def create_client(payload: ClientCreate, db: Session = Depends(get_db)):
    # Vérifier si le client existe déjà
    existing = db.query(Client).filter(Client.code_client == payload.code_client).first()
    if existing:
        raise HTTPException(status_code=400, detail="Client déjà existant")

    api_key = f"KEY-{payload.code_client}"

    client = Client(
        code_client=payload.code_client,
        nom_structure=payload.nom_structure,
        adresse_postale=payload.adresse_postale,
        api_key=api_key,
        date_creation=datetime.now()
    )

    db.add(client)
    db.commit()
    db.refresh(client)

    return {"status": "success", "api_key": api_key, "id_client": client.id_client}

# ---------------------------
# Dépôt de prélèvement (client)
# ---------------------------

@router.post("/measurements")
def create_measurement(
    payload: MeasurementCreate,
    api_key: str = Header(None),
    db: Session = Depends(get_db)
):
    client = verify_api_key(api_key, db)

    measurement = Measurement(
        id_client=client.id_client,
        date_prelevement=datetime.now(),
        lieu_prelevement="API",
        ph=payload.ph,
        hardness=payload.hardness,
        solids=payload.solids,
        chloramines=payload.chloramines,
        sulfate=payload.sulfate,
        conductivity=payload.conductivity,
        organic_carbon=payload.organic_carbon,
        trihalomethanes=payload.trihalomethanes,
        turbidity=payload.turbidity,
        provenance="Saisie",
        created_at=datetime.now()
    )

    db.add(measurement)
    db.commit()
    db.refresh(measurement)

    return {"status": "success", "id_measurement": measurement.id_measurement}

# ---------------------------
# Consultation client
# ---------------------------

@router.get("/measurements")
def get_measurements(api_key: str = Header(None), db: Session = Depends(get_db)):
    client = verify_api_key(api_key, db)
    data = db.query(Measurement).filter(Measurement.id_client == client.id_client).all()
    return data

# ---------------------------
# Consultation admin/expert
# ---------------------------

@router.get("/measurements/admin")
def get_all_measurements(db: Session = Depends(get_db)):
    return db.query(Measurement).all()
