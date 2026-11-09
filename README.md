# 📊 SSH Log Analyzer

Bienvenue sur mon projet d'analyse de logs SSH ! J'ai développé ce pipeline ETL (Extraction, Transformation, Chargement) complet et modulaire dans le cadre de mes études en Ingénierie des Données.

L'objectif de ce projet est de partir d'un volume massif de logs d'authentification bruts (`auth.log` - plus de **65 565 lignes**) afin d'extraire, géolocaliser et stocker les tentatives d'accès SSH pour générer un tableau de bord analytique de sécurité.

---

## 🛠️ Stack Technique & Architecture

* **Gestionnaire de projet & Environnement :** `uv`
* **Langage & Traitement :** Python (Regex, `pandas`)
* **Base de Données :** PostgreSQL (`psycopg2-binary`)
* **Géolocalisation & Optimisation :** API `ipinfo.io` + **Cache en mémoire** (In-Memory Caching & Rate-Limit Handling)
* **Visualisation (Serving) :** `matplotlib`

---

## ✨ Fonctionnalités Majeures du Pipeline

* **Ingestion & Parsing (`ingestion/raw.py`, `process/extract_transform.py`) :** Parcours des fichiers de logs bruts et extraction structurée (Mois, Jour, Heure, IP, Port, Message) via expressions régulières (Regex).
* **Géolocalisation Haute Performance (`process/geolocation.py`) :** 
  * Intégration d'un **système de cache en mémoire** (`IP_CACHE`) pour mémoriser les adresses IP déjà interrogées. Cela évite les requêtes redondantes et permet d'insérer plus de 65 000 lignes en quelques minutes.
  * Gestion automatique du **Rate Limiting (HTTP 429)** de l'API `ipinfo.io` sans interrompre l'exécution du script.
* **Stockage Relationnel PostgreSQL (`storage/database.py`) :**
  * Migration réussie de SQLite vers **PostgreSQL** (`log_analysis`).
  * Réinitialisation propre de la table via `TRUNCATE TABLE ssh_logs RESTART IDENTITY`.
  * Sauvegarde progressive (`commit` par lots de 1 000 lignes) pour garantir l'intégrité et la rapidité du traitement.
* **Dashboard Analytics & Visualisation (`serving/dashboard.py`) :**
  * Connexion directe à PostgreSQL via `psycopg2` et requêtage optimisé avec `pandas`.
  * Nettoyage et filtrage dynamique des métriques pour exclure le trafic local (`127.0.0.1`, `Local`) et les limites d'API (`Limit_Reached`).
  * Génération automatique d'un tableau de bord visuel `matplotlib` affichant :
    1. **Top 10 des Pays** d'origine des attaques.
    2. **Top 10 des Adresses IP** les plus agressives.
    3. **Top 10 des Ports** les plus ciblés.

---

## 📂 Structure du Projet

```text
log_analyzer/
├── data/                  # Fichiers de logs bruts (auth.log, auth.log.1, etc.)
├── ingestion/
│   └── raw.py             # Lecture et extraction brute des lignes
├── process/
│   ├── extract_transform.py # Extraction Regex des champs
│   └── geolocation.py     # API ipinfo.io avec cache & gestion 429
├── storage/
│   └── database.py        # Connexion PostgreSQL & insertion par lots
├── serving/
│   └── dashboard.py       # Récupération pandas & visualisations matplotlib
└── README.md

🚀 Comment lancer le projet ?
1. Prérequis & Base de données
Assurez-vous d'avoir une instance PostgreSQL en cours d'exécution avec la base de données log_analysis créée (utilisateur postgres, mot de passe 123).

Placez vos fichiers de logs (ex: auth.log, auth.log.1, etc.) dans un dossier nommé data/ à la racine du projet.

2. Gestion des dépendances avec uv
Installez les bibliothèques requises :

Bash
uv add psycopg2-binary pandas matplotlib requests

3. Exécution du Pipeline ETL (Insertion dans PostgreSQL)
Lancez l'exécution du module de stockage pour créer la table et insérer l'intégralité des 65 565 lignes :

Bash
uv run python -m storage.database

4. Affichage du Tableau de Bord Analytique
Une fois les données insérées dans PostgreSQL, lancez cette commande pour afficher les graphiques de sécurité :

Bash
uv run python -m serving.dashboard

👨‍💻 Auteur

Mohammed Ziad — Étudiant en Ingénierie Logicielle-ESISA