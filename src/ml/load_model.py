import os
import joblib

MODEL_PATH = "models/model_xgboost_safe.pkl"
SCALER_PATH = "models/scaler.pkl"
THRESHOLD_PATH = "models/threshold_safe.pkl"

def load_model():
    model = None
    scaler = None
    threshold = None

    try:
        # ---------------------------
        # Charger le modèle calibré
        # ---------------------------
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            print(f"✔ Modèle calibré chargé depuis {MODEL_PATH}")
        else:
            print("⚠ Aucun modèle trouvé.")

        # ---------------------------
        # Charger le scaler
        # ---------------------------
        if os.path.exists(SCALER_PATH):
            scaler = joblib.load(SCALER_PATH)
            print(f"✔ Scaler chargé depuis {SCALER_PATH}")
        else:
            print("⚠ Aucun scaler trouvé.")

        # ---------------------------
        # Charger le seuil
        # ---------------------------
        if os.path.exists(THRESHOLD_PATH):
            threshold = joblib.load(THRESHOLD_PATH)
            print(f"✔ Seuil chargé depuis {THRESHOLD_PATH}")
        else:
            print("⚠ Aucun seuil trouvé.")

    except Exception as e:
        print(f"❌ Erreur lors du chargement du modèle : {e}")

    return model, scaler, threshold
