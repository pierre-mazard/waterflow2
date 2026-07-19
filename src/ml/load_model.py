import mlflow
import os
import pickle

MODEL_PATH = os.getenv("MODEL_PATH", "models/model.pkl")
MODEL_VERSION = os.getenv("MODEL_VERSION", "v1")

def load_model():
    """
    Charge le modèle depuis un fichier .pkl ou depuis MLflow.
    """
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        print(f"✔ Modèle chargé depuis {MODEL_PATH}")
        return model

    # Option MLflow (si activé plus tard)
    try:
        model = mlflow.pyfunc.load_model(f"models:/{MODEL_VERSION}")
        print(f"✔ Modèle chargé depuis MLflow (version {MODEL_VERSION})")
        return model
    except Exception as e:
        print("❌ Impossible de charger le modèle :", e)
        raise
