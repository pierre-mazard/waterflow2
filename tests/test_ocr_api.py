from unittest.mock import patch

def fake_extract_text(path):
    return """
    pH: 7.3
    Hardness: 190
    Solids: 11000
    Chloramines: 6.2
    Sulfate: 340
    Conductivity: 460
    Organic_carbon: 11
    Trihalomethanes: 75
    Turbidity: 3.2
    """

def test_ocr_upload(client):
    # Création client
    resp = client.post(
        "/api/clients",
        params={
            "code_client": "OCR-01",
            "nom_structure": "OCR Structure",
            "adresse_postale": "OCR Adresse"
        }
    )
    api_key = resp.json()["api_key"]

    # Mock OCR
    with patch("src.ocr.ocr_service.extract_text_from_file", fake_extract_text):
        file_content = b"fake pdf content"
        response = client.post(
            "/api/ocr/lab-report",
            headers={"api_key": api_key},
            files={"file": ("test.pdf", file_content, "application/pdf")}
        )

    assert response.status_code == 200
    assert "id_measurement" in response.json()
    assert response.json()["extracted_fields"]["ph"] == 7.3
