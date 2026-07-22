import os
import pandas as pd
import numpy as np
import shap
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.calibration import CalibratedClassifierCV
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
import xgboost as xgb
from pathlib import Path
import joblib

# ============================================================
# MLflow – Backend professionnel SQLite
# ============================================================
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("waterflow_potability")

# ============================================================
# Paths
# ============================================================
MODEL_PATH = Path("models/model_xgboost_safe.pkl")
SCALER_PATH = Path("models/scaler.pkl")
THRESHOLD_PATH = Path("models/threshold_safe.pkl")
FEATURE_IMPORTANCES_PATH = Path("models/feature_importances_xgboost.csv")
EXPLANATION_PATH = Path("models/example_explanation.csv")
DATA_PATH = Path("data/features/water_features_optimized.csv")

# ============================================================
# Load dataset
# ============================================================
print("📥 Chargement du dataset...")
df = pd.read_csv(DATA_PATH)

# ============================================================
# Ajouter les features OMS/EPA
# ============================================================
print("🧪 Ajout des indicateurs OMS/EPA...")

df["risk_chloramines"] = (df["Chloramines"] > 4).astype(int)
df["risk_thm"] = (df["Trihalomethanes"] > 80).astype(int)
df["risk_turbidity"] = (df["Turbidity"] > 5).astype(int)
df["risk_ph"] = ((df["ph"] < 6.5) | (df["ph"] > 8.5)).astype(int)
df["risk_tds"] = (df["Solids"] > 1000).astype(int)
df["risk_sulfate"] = (df["Sulfate"] > 250).astype(int)
df["risk_conductivity"] = (df["Conductivity"] > 800).astype(int)

# ============================================================
# Features + target
# ============================================================
X = df.drop(columns=["Potability"])
y = df["Potability"]

# ============================================================
# Split stratifié
# ============================================================
print("🔀 Split train/test stratifié...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# ============================================================
# SMOTE pour rééquilibrer
# ============================================================
print("⚖️ Rééquilibrage SMOTE...")
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# ============================================================
# Normalisation
# ============================================================
print("📏 Normalisation...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_res)
X_test_scaled = scaler.transform(X_test)

# ============================================================
# Modèle XGBoost régularisé
# ============================================================
print("🤖 Entraînement du modèle XGBoost régularisé...")

model = XGBClassifier(
    n_estimators=300,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.5,
    reg_lambda=1.0,
    gamma=0.5,
    random_state=42
)

# ============================================================
# Calibration des probabilités
# ============================================================
calibrated_model = CalibratedClassifierCV(model, cv=5)
calibrated_model.fit(X_train_scaled, y_train_res)

train_score = calibrated_model.score(X_train_scaled, y_train_res)
test_score = calibrated_model.score(X_test_scaled, y_test)

print(f"📊 Score train : {train_score:.3f}")
print(f"📈 Score test : {test_score:.3f}")

# ============================================================
# Calcul du seuil de sécurité
# ============================================================
print("🛡 Calcul du seuil de sécurité...")

probas_train = calibrated_model.predict_proba(X_train_scaled)[:, 1]
threshold = np.quantile(probas_train, 0.85)

print(f"✔ Nouveau seuil de sécurité = {threshold:.3f}")

# ============================================================
# SHAP natif XGBoost (avant calibration)
# ============================================================
print("📘 Calcul des explications SHAP...")

model.fit(X_train_scaled, y_train_res)

sample = shap.sample(X_train_scaled, 100)
dtrain = xgb.DMatrix(sample, feature_names=X.columns.tolist())

shap_values = model.get_booster().predict(
    dtrain,
    pred_contribs=True
)

example_shap = shap_values[0][:-1]

pd.DataFrame({
    "feature": X.columns,
    "shap_value": example_shap
}).to_csv(EXPLANATION_PATH, index=False)

print(f"✔ Explication SHAP sauvegardée dans {EXPLANATION_PATH}")

# ============================================================
# Importances
# ============================================================
importances = model.feature_importances_
pd.DataFrame({
    "feature": X.columns,
    "importance": importances
}).to_csv(FEATURE_IMPORTANCES_PATH, index=False)

print(f"✔ Importances sauvegardées dans {FEATURE_IMPORTANCES_PATH}")

# ============================================================
# Sauvegarde des artefacts
# ============================================================
joblib.dump(calibrated_model, MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)
joblib.dump(threshold, THRESHOLD_PATH)

print("🎉 Modèle, scaler et seuil sauvegardés !")

# ============================================================
# MLflow logging
# ============================================================
with mlflow.start_run():
    mlflow.log_metric("train_score", train_score)
    mlflow.log_metric("test_score", test_score)
    mlflow.log_metric("threshold", float(threshold))

    mlflow.log_artifact(str(MODEL_PATH))
    mlflow.log_artifact(str(SCALER_PATH))
    mlflow.log_artifact(str(THRESHOLD_PATH))
    mlflow.log_artifact(str(FEATURE_IMPORTANCES_PATH))
    mlflow.log_artifact(str(EXPLANATION_PATH))

print("🏁 Entraînement terminé et loggé dans MLflow (SQLite) !")
