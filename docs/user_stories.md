# Waterflow 2 — User Stories

## 👤 Profil : Client final

> « Les clients veulent déposer leurs prélèvements et récupérer leurs résultats via une API simple, sécurisée par une clé API. »

### User Story 1 — Création de compte client  
En tant que client, je veux qu’un administrateur crée mon compte (ID, nom, adresse) afin d’obtenir une clé API pour utiliser la plateforme.

### User Story 2 — Dépôt de prélèvement  
En tant que client, je veux envoyer un prélèvement structuré via une route API sécurisée par ma clé API, afin d’obtenir une prédiction de potabilité.

### User Story 3 — Consultation de mes prélèvements  
En tant que client, je veux consulter uniquement mes prélèvements via API, afin de suivre mes analyses.

### User Story 4 — Dépôt de fiche labo (OCR)  
En tant que client, je veux envoyer une photo/PDF d’une fiche labo via une route API, afin que la plateforme extraie automatiquement les mesures et crée un prélèvement.

---

## 👨‍🔬 Profil : Analyste qualité

> « Les analystes veulent une plateforme unique pour consulter les prélèvements, les prédictions et les métriques du modèle. »

### User Story 5 — Dashboard expert  
En tant qu’analyste, je veux accéder à un dashboard regroupant tous les prélèvements, leurs provenances (Saisie/OCR), et les prédictions.

### User Story 6 — Filtres avancés  
En tant qu’analyste, je veux filtrer par client, date, provenance, résultat, afin de mener des analyses ciblées.

---

## 🧑‍💼 Profil : Responsable d’exploitation

> « Le responsable veut superviser la santé globale de la plateforme : erreurs, temps de réponse, volumes, alertes. »

### User Story 7 — Monitoring système  
En tant que responsable, je veux voir les métriques système (requêtes, erreurs, latence), afin de surveiller la santé de la plateforme.

### User Story 8 — Gestion des clés API  
En tant que responsable, je veux générer / régénérer les clés API des clients.

### User Story 9 — Journalisation des accès  
En tant que responsable, je veux consulter un journal des accès (clé API, endpoint, statut), pour la traçabilité RGPD.

---

## 🔐 Critères d’acceptation 

- Chaque client ne peut voir que ses données.  
- Les routes client sont sécurisées par clé API.  
- Les routes admin/expert sont sécurisées par un token serveur.  

### Dashboard expert

- Affiche : prélèvements, provenance, prédictions, métriques modèle.

### Monitoring

- Affiche : nombre de requêtes, erreurs, temps de réponse.

### Système OCR

- Accepte : PDF / JPG / PNG.  
- Extrait les champs (date, mesures).  
- Crée un prélèvement structuré.
