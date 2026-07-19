import os
import pickle

MODEL_PATH = "models/model.pkl"

def load_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        print(f"✔ Modèle chargé depuis {MODEL_PATH}")
        return model

    print("⚠ Aucun modèle trouvé. L'API démarre sans modèle.")
    return None
