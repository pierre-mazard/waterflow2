from fastapi import APIRouter, UploadFile, File, Depends, Header, HTTPException
from sqlalchemy.orm import Session
import tempfile
from datetime import datetime

from src.db.database import get_db
from src.db.models import Measurement, Client
from src.ocr.ocr_service import extract_text_from_file, parse_lab_report

router = APIRouter()

def verify_api_key(api_key: str, db: Session):
    client = db.query(Client).filter(Client.api_key == api_key).first()
    if not client:
        raise HTTPException(status_code=401, detail="Clé API invalide")
    return client

@router.post("/ocr/lab-report")
async def upload_lab_report(
    file: UploadFile = File(...),
    api_key: str = Header(None),
    db: Session = Depends(get_db)
):
    client = verify_api_key(api_key, db)

    # Sauvegarde temporaire du fichier
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # OCR
    try:
        text = extract_text_from_file(tmp_path)
        fields = parse_lab_report(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR error: {str(e)}")

    # Vérification des champs extraits
    if any(v is None for v in fields.values()):
        raise HTTPException(status_code=400, detail="Impossible d'extraire toutes les mesures")

    # Insertion dans la DB
    measurement = Measurement(
        id_client=client.id_client,
        date_prelevement=datetime.now(),
        lieu_prelevement="OCR",
        provenance="OCR",
        created_at=datetime.now(),
        **fields
    )

    db.add(measurement)
    db.commit()

    return {
        "status": "success",
        "id_measurement": measurement.id_measurement,
        "extracted_fields": fields
    }
