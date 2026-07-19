def test_predict(client):
    payload = {
        "ph": 7.2,
        "hardness": 180,
        "solids": 12000,
        "chloramines": 6.5,
        "sulfate": 350,
        "conductivity": 450,
        "organic_carbon": 12,
        "trihalomethanes": 80,
        "turbidity": 3.5
    }

    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json()
