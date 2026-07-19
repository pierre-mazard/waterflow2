from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from src.db.database import get_db
from src.db.models import Client, Measurement

router = APIRouter()

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
def create_client(code_client: str, nom_structure: str, adresse_postale: str, db: Session = Depends(get_db)):
    api_key = f"KEY-{code_client}"

    client = Client(
        code_client=code_client,
        nom_structure=nom_structure,
        adresse_postale=adresse_postale,
        api_key=api_key,
        date_creation=datetime.now()
    )

    db.add(client)
    db.commit()

    return {"status": "success", "api_key": api_key}

# ---------------------------
# Dépôt de prélèvement (client)
# ---------------------------
@router.post("/measurements")
def create_measurement(
    ph: float,
    hardness: float,
    solids: float,
    chloramines: float,
    sulfate: float,
    conductivity: float,
    organic_carbon: float,
    trihalomethanes: float,
    turbidity: float,
    api_key: str = Header(None),
    db: Session = Depends(get_db)
):
    client = verify_api_key(api_key, db)

    measurement = Measurement(
        id_client=client.id_client,
        date_prelevement=datetime.now(),
        lieu_prelevement="API",
        ph=ph,
        hardness=hardness,
        solids=solids,
        chloramines=chloramines,
        sulfate=sulfate,
        conductivity=conductivity,
        organic_carbon=organic_carbon,
        trihalomethanes=trihalomethanes,
        turbidity=turbidity,
        provenance="Saisie",
        created_at=datetime.now()
    )

    db.add(measurement)
    db.commit()

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
