# Note RGPD — Waterflow 2

## 1. Introduction

La plateforme Waterflow 2 traite des données liées à la qualité de l’eau ainsi que des informations permettant d’identifier les clients de la collectivité.  
Cette note décrit :

- les données personnelles collectées,
- les finalités du traitement,
- les mécanismes de sécurité,
- la journalisation des accès,
- les durées de conservation,
- la gestion des clés API,
- les mesures de minimisation et de protection.

Elle s’inscrit dans le cadre du RGPD (Règlement Général sur la Protection des Données).

---

## 2. Données personnelles collectées

### 2.1. Données d’identification du client

| Champ | Description | Catégorie |
|-------|-------------|-----------|
| `code_client` | Identifiant lisible (ex : CLIENT-042) | Donnée personnelle indirecte |
| `nom_structure` | Nom de l’organisation cliente | Donnée personnelle |
| `adresse_postale` | Adresse de la structure | Donnée personnelle |
| `api_key` | Clé API unique | Identifiant technique |

### 2.2. Données non personnelles

Les mesures physico-chimiques de l’eau (pH, dureté, nitrates, etc.) **ne sont pas des données personnelles**.

---

## 3. Finalités du traitement

Les données personnelles sont utilisées uniquement pour :

- identifier le client appelant l’API,
- sécuriser l’accès aux prélèvements,
- garantir la traçabilité des actions (journalisation),
- permettre la gestion des clés API (création, régénération),
- fournir un historique des prélèvements associés à un client.

Aucune donnée n’est utilisée à des fins commerciales ou de profilage.

---

## 4. Minimisation des données

Conformément au RGPD :

- seules les données strictement nécessaires sont collectées,
- aucune donnée sensible (santé, religion, etc.) n’est stockée,
- les données personnelles sont limitées à l’identification du client,
- les mesures d’eau ne contiennent aucune information personnelle.

---

## 5. Journalisation des accès (ACCESS_LOG)

La plateforme journalise chaque appel API via la table `access_logs` :

| Champ | Description |
|-------|-------------|
| `api_key` | Identifie le client appelant |
| `endpoint` | Route appelée |
| `status_code` | Résultat de la requête |
| `duration_ms` | Temps de traitement |
| `timestamp` | Date et heure |

### Finalités de la journalisation

- sécurité,
- audit RGPD,
- détection d’incidents,
- supervision du système.

### Durée de conservation recommandée

- **12 mois** pour les logs techniques,
- **36 mois** pour les logs d’accès si exigé par la collectivité.

Les durées peuvent être adaptées selon les politiques internes.

---

## 6. Sécurité et confidentialité

### 6.1. Clé API

Chaque client possède une clé API unique :

- générée par un administrateur,
- stockée de manière sécurisée,
- jamais transmise en clair dans les journaux,
- régénérable en cas de compromission.

### 6.2. Accès aux données

- Un client ne peut accéder **qu’à ses propres prélèvements**.
- Les analystes qualité ont accès à **tous les prélèvements**.
- Le responsable d’exploitation a accès aux **journaux d’accès**.

### 6.3. Transmission

- Toutes les communications doivent être effectuées via HTTPS.
- Les fichiers envoyés à l’API OCR sont transmis via un canal sécurisé.

---

## 7. Gestion des clés API

### Création

- via `POST /api/clients` (admin),
- génération d’une clé API aléatoire (token sécurisé),
- stockage dans la base.

### Régénération

- via une route admin dédiée,
- invalide immédiatement l’ancienne clé,
- journalisation de l’opération dans `access_logs`.

### Compromission

En cas de compromission :

1. régénération immédiate de la clé,
2. notification au client,
3. analyse des journaux d’accès,
4. documentation de l’incident (voir `docs/incident_scenario.md`).

---

## 8. Droits des personnes

Les clients peuvent demander :

- la consultation des données personnelles associées à leur compte,
- la suppression de leur compte (si compatible avec les obligations légales),
- la régénération de leur clé API,
- des informations sur les durées de conservation.

---

## 9. Conclusion

La plateforme Waterflow 2 respecte les principes RGPD :

- minimisation,
- sécurité,
- traçabilité,
- confidentialité,
- limitation des finalités.



