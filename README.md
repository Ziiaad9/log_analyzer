# 📊 SSH Log Analyzer

Bienvenue sur mon projet d'analyse de logs SSH ! J'ai développé ce pipeline ETL (Extraction, Transformation, Chargement) de zéro dans le cadre de mon projet d'ingénierie des données à l'EST Fès. 

L'objectif de ce projet est de partir de fichiers de logs d'authentification bruts (`auth.log`) pour en extraire des statistiques de sécurité claires et visuelles. J'ai fait le choix d'utiliser un minimum de bibliothèques externes pour garder le projet léger et montrer la maîtrise des outils standards de Python.

## ✨ Ce que fait le code

* **Parsing (Ingestion & Extraction) :** Je parcours les fichiers de logs bruts et j'extrais les informations essentielles (Date, Heure, IP, Port, Message) en utilisant des expressions régulières (Regex).
* **Géolocalisation & Cache :** J'utilise l'API `ipinfo.io` pour identifier le pays d'origine des adresses IP. Comme l'API limite le nombre de requêtes, j'ai mis en place un système de **cache en mémoire**. Cela permet de ne jamais interroger l'API deux fois pour la même IP, évitant ainsi les blocages et accélérant drastiquement le traitement !
* **Stockage :** Une fois les données nettoyées et géolocalisées, elles sont sauvegardées proprement dans une base de données relationnelle locale `SQLite` (`logs_analysis.db`).
* **Dashboard (Serving) :** Un script dédié interroge la base de données via SQL et génère un tableau de bord interactif avec `matplotlib` affichant 3 métriques clés :
  1. Le nombre de tentatives échouées par pays.
  2. Le nombre de tentatives réussies par utilisateur.
  3. Le nombre de tentatives échouées avec "invalid user" par pays.

## 📂 Prérequis de structure

Pour que le projet fonctionne correctement, assurez-vous de placer vos fichiers de logs (ex: `auth.log`, `auth.log.1`, `auth.log.2`, etc.) à l'intérieur d'un dossier nommé **`data/`** situé à la racine du projet.

## 🚀 Comment lancer le projet ?

Vous aurez besoin de Python installé sur votre machine. Suivez ces étapes dans votre terminal :

**1. Installez les dépendances nécessaires :**
```bash
pip install requests matplotlib
```
**2. Lancer le traitement des données (Pipeline ETL) :**

Cette étape va lire le dossier data/, géolocaliser les IPs et remplir la base de données SQLite.

```bash
python storage/database.py 
```

(Patientez quelques secondes le temps du traitement. Un message de succès s'affichera à la fin).

**3. Afficher le tableau de bord analytique :**
Une fois la base de données prête, lancez cette commande pour générer et afficher les graphiques :

```bash
python serving/dashboard.py
```

👨‍💻 Auteur
Mohammed Ziad-Étudiant en Ingénierie Logicielle - ESISA