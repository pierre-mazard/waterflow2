def test_create_client(client):
    response = client.post(
        "/api/clients",
        params={
            "code_client": "TEST-01",
            "nom_structure": "Test Structure",
            "adresse_postale": "Test Adresse"
        }
    )
    assert response.status_code == 200
    assert "api_key" in response.json()

def test_create_measurement(client):
    # Création client
    resp = client.post(
        "/api/clients",
        params={
            "code_client": "TEST-02",
            "nom_structure": "Structure 2",
            "adresse_postale": "Adresse 2"
        }
    )
    api_key = resp.json()["api_key"]

    # Dépôt prélèvement
    response = client.post(
        "/api/measurements",
        headers={"api_key": api_key},
        params={
            "ph": 7.1,
            "hardness": 150,
            "solids": 10000,
            "chloramines": 6.0,
            "sulfate": 300,
            "conductivity": 400,
            "organic_carbon": 10,
            "trihalomethanes": 70,
            "turbidity": 3.0
        }
    )

    assert response.status_code == 200
    assert "id_measurement" in response.json()
