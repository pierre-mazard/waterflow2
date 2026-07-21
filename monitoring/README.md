# Monitoring Waterflow 2

## 1. Architecture

Le monitoring repose sur :

- **Prometheus** : collecte des métriques
- **Grafana** : visualisation
- **FastAPI Instrumentator** : exposition des métriques via `/metrics`

## 2. Métriques disponibles

- latence des endpoints
- nombre de requêtes
- erreurs
- histogrammes de temps de réponse
- métriques OCR
- métriques prédiction
- métriques DB

## 3. Lancer le monitoring

```bash
docker-compose up --build
```

Accès : 

- API : http://localhost:8000
- Prometheus : http://localhost:9090
- Grafana : http://localhost:3000

## Dashboard Grafana

Importer le dahsboard :
- monitoring/grafana/waterflow_dashboard.json

Ce dahsboard affiche : 
- Latence API
- Taux d'erreur
- Prédictions par minute
- OCR par minute
- charge BB
- logs RGPD