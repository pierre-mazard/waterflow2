# Architecture Technique — Waterflow 2

## 1. Vue d’ensemble

Waterflow 2 est une plateforme MLOps complète permettant :

- la gestion des clients via clé API,
- le dépôt de prélèvements structurés,
- l’ingestion automatisée de fiches labo via OCR,
- la prédiction de potabilité via un modèle MLflow,
- la consultation experte via une interface web,
- le monitoring du système et du modèle,
- la traçabilité RGPD des accès.

L’architecture repose sur une **API unique** découpée en trois modules :

- **API Data** : gestion des clients, prélèvements, journaux d’accès.
- **API Model** : prédiction de potabilité via modèle MLflow.
- **API OCR** : ingestion de fiches labo via OCR.space.

---

## 2. Schéma global (conceptuel)

```text
Client (clé API)
    |
    v
+------------------+
|   API Unique     |
|    (FastAPI)     |
|                  |
|  /api/clients    |
|  /api/measurements
|  /api/predict    |
|  /api/ocr/lab-report
+------------------+
    |      |       |
    v      v       v
Base SQL   Modèle MLflow   OCR.space API
(PostgreSQL) (tracking + registry)

```
---

## 3. Modules de l’API

### 3.1. API Data

Fonctions principales :

- création de clients (admin),
- génération/régénération de clés API,
- dépôt de prélèvements,
- consultation filtrée des prélèvements,
- journalisation des accès (RGPD).

Routes :

- `POST /api/clients`
- `GET /api/clients`
- `POST /api/measurements`
- `GET /api/measurements`
- `GET /api/measurements/admin`

Sécurité :

- Clients → clé API  
- Experts → token serveur

---

### 3.2. API Model

Fonctions :

- chargement du modèle MLflow,
- prédiction de potabilité,
- renvoi des métadonnées (version modèle, scores),
- tests unitaires et d’intégration.

Route :

- `POST /api/predict`

---

### 3.3. API OCR

Fonctions :

- réception d’un fichier (PDF/JPG/PNG),
- appel à OCR.space,
- extraction des champs (date, mesures),
- création d’un prélèvement structuré,
- renvoi de l’ID du prélèvement.

Route :

- `POST /api/ocr/lab-report`

---

## 4. Base de données (PostgreSQL)

### Tables principales :

- **clients**
- **measurements**
- **access_logs**

### Contraintes :

- clé API unique par client,
- FK client → prélèvements,
- journaux d’accès pour traçabilité RGPD,
- provenance : `"Saisie"` ou `"OCR"`.

---

## 5. Modèle MLflow

- tracking des expériences,
- enregistrement du modèle,
- chargement via MLflow Model Registry,
- métriques : accuracy, precision, recall, f1,
- monitoring du modèle (latence, erreurs, version).

---

## 6. Interface web expert (Streamlit)

Fonctions :

- tableau des prélèvements,
- filtres avancés,
- affichage des prédictions,
- affichage des métriques du modèle,
- affichage des journaux d’accès.

---

## 7. Monitoring

### Monitoring système :

- nombre de requêtes,
- temps de réponse,
- taux d’erreur,
- logs structurés.

### Monitoring modèle :

- latence de prédiction,
- erreurs,
- version du modèle,
- métriques MLflow.

---

## 8. Conteneurisation (Docker)

Services :

- `api` (FastAPI)
- `db` (PostgreSQL)
- `web` (Streamlit)
- [optionnel] `mlflow`

Fichiers :

- `docker/Dockerfile.api`
- `docker/Dockerfile.web`
- `docker/docker-compose.yml`

---

## 9. CI/CD (GitHub Actions)

Pipeline minimal :

- installation des dépendances,
- exécution des tests PyTest,
- vérification du formatage,
- build Docker (optionnel),
- déploiement (optionnel).

Fichier :

- `.github/workflows/tests.yml`

---

## 10. RGPD

- séparation stricte des périmètres (clé API),
- minimisation des données personnelles,
- journalisation des accès,
- documentation des durées de conservation,
- régénération des clés API en cas de compromission.

