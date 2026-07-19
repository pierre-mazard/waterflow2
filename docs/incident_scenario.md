# Scénario d’incident — Waterflow 2 (E5)

## 1. Contexte de l’incident

Le 12/07/2026, plusieurs clients signalent que l’API OCR (`POST /api/ocr/lab-report`) renvoie systématiquement une erreur :

503 Service Unavailable — OCR provider unreachable


Les analystes constatent également que les prélèvements provenant de l’OCR n’apparaissent plus dans le dashboard expert.

Cet incident bloque une fonctionnalité critique : l’ingestion automatisée des fiches labo.

---

## 2. Détection de l’incident

### 2.1. Logs applicatifs

Les logs montrent une augmentation soudaine des erreurs :

ERROR ocr_service: OCR request failed (timeout)
ERROR ocr_service: Provider unreachable


### 2.2. Monitoring système

- Taux d’erreur OCR : **92%**  
- Temps de réponse OCR : **> 10 secondes**  
- Requêtes OCR : stable  
- Requêtes Data/Model : normales

### 2.3. Journalisation RGPD

Les journaux `access_logs` montrent :

| api_key | endpoint | status_code | timestamp |
|--------|----------|-------------|-----------|
| CLIENT-042 | /api/ocr/lab-report | 503 | 12/07/2026 09:14 |
| CLIENT-017 | /api/ocr/lab-report | 503 | 12/07/2026 09:15 |

---

## 3. Diagnostic

### Hypothèses analysées :

1. **Clé API OCR.space invalide**  
2. **Timeout réseau entre Waterflow 2 et OCR.space**  
3. **Format du fichier envoyé incorrect**  
4. **Bug dans le parsing JSON de la réponse OCR**  
5. **Incident côté OCR.space (service externe)**

### Vérifications effectuées :

- Test manuel via `curl` → **échec**  
- Test via interface OCR.space → **succès**  
- Vérification `.env` → clé API correcte  
- Vérification du code → parsing JSON correct  
- Vérification du firewall → OK

### Diagnostic final :

> Le service OCR.space a modifié son endpoint d’API (migration vers `v4`).  
> L’ancienne URL `https://api.ocr.space/parse/image` renvoie désormais une erreur 503.

---

## 4. Correction

### 4.1. Mise à jour du code

Dans `src/ocr/ocr_service.py` :

```diff
- OCR_URL = "https://api.ocr.space/parse/image"
+ OCR_URL = "https://api.ocr.space/parse/image/v4"
```

### 4.2 Mise à jour du timeout
```diff
- timeout=5
+ timeout=15
```

### 4.3 Ajout d'un fallback automatique

Si OCR.space renvoie une erreur → réessai 1 fois → log détaillé → réponse propre au client.

## 5. Vérification 

### 5.1 Test unitaires

Ajout dans tests/test_ocr_api.py :

- mock de la réponse OCR v4

- test de parsing

- test de création de prélèvement

### 5.2 Tests d'intégration 

- envoi d’un PDF réel → extraction OK

- création d’un prélèvement → OK

- prédiction via /api/predict → OK

### 5.3 TEest end-to-end

```Code
PDF → OCR → mesures → prélèvement → prédiction → dashboard expert
```
Résultat : succès complet

## 6. Déploiement 

### 6.1 CI/CD

Le pipeline GitHub Actions exécute :

- installation des dépendances

- tests PyTest

- build Docker

- déploiement 

### 6.2 Vesioning

- Branche : feature/fix-ocr-endpoint

- Commit : fix: update OCR endpoint to v4 + improved timeout

- Merge request → develop

- Merge → main après validation

## 7 Documentation 

Les fichiers mis à jour : 

- docs/architecture.md → mise à jour du module OCR

- docs/rgpd_note.md → ajout d’un paragraphe sur la gestion des incidents

- CHANGELOG.md → ajout d’une section “Incident OCR — 12/07/2026”

## 8. Conclusion 

L'incident OCR a été : 

- détecté rapidement via les logs et le monitoring,

- diagnostiqué précisément (changement d’endpoint OCR.space),

- corrigé proprement (mise à jour URL + timeout + fallback),

- testé (unitaires, intégration, end-to-end),

- déployé via CI/CD,

- documenté conformément aux exigences RNCP E5.

Ce scénario démontre la capacité de l’équipe à maintenir la plateforme en condition opérationnelle.