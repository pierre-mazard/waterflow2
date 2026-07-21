import os
import pickle

MODEL_PATH = "models/model_xgboost_safe.pkl"
SCALER_PATH = "models/scaler.pkl"
THRESHOLD_PATH = "models/threshold_safe.pkl"

def load_model():
    model = None
    scaler = None
    threshold = None

    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        print(f"✔ Modèle chargé depuis {MODEL_PATH}")
    else:
        print("⚠ Aucun modèle trouvé.")

    if os.path.exists(SCALER_PATH):
        with open(SCALER_PATH, "rb") as f:
            scaler = pickle.load(f)
        print(f"✔ Scaler chargé depuis {SCALER_PATH}")
    else:
        print("⚠ Aucun scaler trouvé.")

    if os.path.exists(THRESHOLD_PATH):
        with open(THRESHOLD_PATH, "rb") as f:
            threshold = pickle.load(f)
        print(f"✔ Seuil chargé depuis {THRESHOLD_PATH}")
    else:
        print("⚠ Aucun seuil trouvé.")

    return model, scaler, threshold
