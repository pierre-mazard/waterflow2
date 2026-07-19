# 📊 Monitoring — Waterflow 2

Ce dossier contient toute la stack de monitoring du projet Waterflow 2 :
- Prometheus pour la collecte des métriques
- Grafana pour la visualisation
- FastAPI Instrumentator pour exposer `/metrics`
- Docker Compose pour orchestrer l’ensemble

## 1. Architecture

FastAPI (/metrics) → Prometheus → Grafana Dashboard

## 2. Fichiers

monitoring/
├── prometheus.yml
├── README.md
└── grafana/
    └── waterflow_dashboard.json

## 3. Configuration Prometheus

```yaml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: "waterflow-api"
    static_configs:
      - targets: ["api:8000"]
```

## 4. Lancer le monitoring

```bash
docker-compose up --build
```

Accès :

- API : http://localhost:8000

- Metrics : http://localhost:8000/metrics

- Prometheus : http://localhost:9090

- Grafana : http://localhost:3000

## 5. Dashboard Grafana

Importer :
monitoring/grafana/waterflow_dashboard.json