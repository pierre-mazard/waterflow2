import requests
import os

OCR_API_KEY = os.getenv("OCR_API_KEY", "YOUR_OCR_KEY")
OCR_URL = "https://api.ocr.space/parse/image"

def extract_text_from_file(file_path: str):
    """
    Envoie un fichier à OCR.space et récupère le texte brut.
    """
    payload = {
        "apikey": OCR_API_KEY,
        "language": "eng"
    }

    with open(file_path, "rb") as f:
        response = requests.post(
            OCR_URL,
            files={"file": f},
            data=payload,
            timeout=30
        )

    data = response.json()

    if data.get("IsErroredOnProcessing"):
        raise Exception(data.get("ErrorMessage"))

    return data["ParsedResults"][0]["ParsedText"]

def parse_lab_report(text: str):
    """
    Extrait les mesures depuis le texte OCR.
    Format attendu dans la fiche labo :
    pH: 7.2
    Hardness: 180
    ...
    """
    fields = {
        "ph": None,
        "hardness": None,
        "solids": None,
        "chloramines": None,
        "sulfate": None,
        "conductivity": None,
        "organic_carbon": None,
        "trihalomethanes": None,
        "turbidity": None
    }

    for line in text.split("\n"):
        line = line.strip()

        for key in fields.keys():
            if line.lower().startswith(key.lower()):
                try:
                    value = float(line.split(":")[1].strip())
                    fields[key] = value
                except:
                    pass

    return fields
