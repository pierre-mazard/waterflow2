# training/train.py

import pandas as pd
import numpy as np
import pickle
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import xgboost as xgb
import shap

DATA_PATH = Path("data/features/water_features_optimized.csv")

MODEL_PATH = Path("models/model_xgboost_safe.pkl")  # on garde le même nom pour compatibilité API
SCALER_PATH = Path("models/scaler.pkl")
THRESHOLD_PATH = Path("models/threshold_safe.pkl")
FEATURE_IMPORTANCES_PATH = Path("models/feature_importances_xgboost.csv")
EXPLANATION_PATH = Path("models/example_explanation.csv")

def main():
    print("📥 Chargement du dataset optimisé...")
    df = pd.read_csv(DATA_PATH)

    feature_cols = [
        "ph",
        "Hardness",
        "Solids",
        "Chloramines",
        "Sulfate",
        "Conductivity",
        "Organic_carbon",
        "Trihalomethanes",
        "Turbidity",
        "interaction_tds_cond",
        "interaction_ph_carbon",
        "interaction_turb_thm"
    ]

    target_col = "Potability"

    X = df[feature_cols]
    y = df[target_col]

    print("🔀 Split train/test...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("📏 Normalisation des features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("🤖 Entraînement du modèle XGBoost...")
    model = xgb.XGBClassifier(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=42,
        eval_metric="logloss"
    )

    model.fit(X_train_scaled, y_train)

    print("📊 Score train :", model.score(X_train_scaled, y_train))
    print("📈 Score test :", model.score(X_test_scaled, y_test))

    # -----------------------------
    # 🔥 Seuil de sécurité
    # -----------------------------
    print("🛡 Calcul du seuil de sécurité...")

    y_proba = model.predict_proba(X_train_scaled)[:, 1]
    threshold = np.quantile(y_proba, 0.99)

    print(f"✔ Seuil de sécurité = {threshold}")

    # -----------------------------
    # 🔍 SHAP explanations
    # -----------------------------
    print("📘 Calcul des explications SHAP...")

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_train_scaled)

    example_explanation = pd.DataFrame(
        shap_values[1][0],
        index=feature_cols,
        columns=["shap_value"]
    )
    example_explanation.to_csv(EXPLANATION_PATH)
    print(f"✔ Explication SHAP sauvegardée dans {EXPLANATION_PATH}")

    # -----------------------------
    # 📊 Importances des features
    # -----------------------------
    print("📊 Sauvegarde des importances de features...")

    importances = pd.DataFrame({
        "feature": feature_cols,
        "importance": model.feature_importances_
    }).sort_values(by="importance", ascending=False)

    importances.to_csv(FEATURE_IMPORTANCES_PATH, index=False)
    print(f"✔ Importances sauvegardées dans {FEATURE_IMPORTANCES_PATH}")

    # -----------------------------
    # 💾 Sauvegarde des artefacts
    # -----------------------------
    MODEL_PATH.parent.mkdir(exist_ok=True)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    with open(SCALER_PATH, "wb") as f:
        pickle.dump(scaler, f)

    with open(THRESHOLD_PATH, "wb") as f:
        pickle.dump(threshold, f)

    print("🎉 Tous les artefacts ont été sauvegardés !")
    print(f"✔ Modèle : {MODEL_PATH}")
    print(f"✔ Scaler : {SCALER_PATH}")
    print(f"✔ Seuil : {THRESHOLD_PATH}")

if __name__ == "__main__":
    main()
