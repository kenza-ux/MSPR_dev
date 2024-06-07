# Structure du Projet 📂

Le projet est organisé de manière à suivre les meilleures pratiques de développement pour une application Flask. Voici un aperçu de la structure du projet avec des explications et des justifications pour chaque dossier et fichier.

## Structure Générale 🌳

MS_CLIENT/
│
├── .env
├── config.py
├── run.py
├── requirements.txt
│
├── app/
│ ├── init.py
│ ├── models.py
│ ├── routes.py
│ ├── utils/
│ │ ├── init.py
│ │ ├── client_api.py
│ │ └── logging_config.py
│ └── templates/
│ └── static/
│
├── migrations/
└── tests/
├── init.py
└── test_db_connection.py



## Détails des Dossiers et Fichiers 📄

### Dossier Racine 🏠

- **`.env`** : Fichier contenant les variables d'environnement. Utilisé pour configurer les informations sensibles comme les identifiants de la base de données.
- **`config.py`** : Fichier de configuration. Contient la classe `Config` qui charge les configurations depuis les variables d'environnement.
- **`run.py`** : Point d'entrée de l'application. Utilisé pour démarrer l'application Flask.

### Dossier `app/` 🗂️

- **`__init__.py`** : Initialise l'application Flask et configure les extensions comme SQLAlchemy et le logger. Contient la fonction `create_app()`.

- **`models.py`** : Définit les modèles de base de données avec SQLAlchemy. Ici, nous avons le modèle `Client`.

- **`routes.py`** : Définit les routes de l'application. Utilise les modèles définis pour interagir avec la base de données et renvoyer des réponses JSON.

- **Dossier `utils/`** : Contient des modules utilitaires.
  - **`__init__.py`** : Fichier d'initialisation pour le module utils.
  - **`client_api.py`** : Contient des fonctionnalités API spécifiques au client.
  - **`logging_config.py`** : Configure le logger pour l'application Flask avec un format coloré.

- **Dossier `templates/`** : Contient les fichiers HTML pour le rendu côté serveur (si nécessaire).

- **Dossier `static/`** : Contient les fichiers statiques comme CSS, JavaScript, images.

### Dossier `migrations/` 🛠️

- Contient les fichiers de migration de la base de données. Utilisé par des outils comme Flask-Migrate pour gérer les changements de schéma de base de données.

### Dossier `tests/` 🧪

- **`__init__.py`** : Fichier d'initialisation pour le module de tests.
- **`test_db_connection.py`** : Contient un script pour tester la connexion à la base de données.

## Justifications ✅

- **Séparation des préoccupations** : En séparant le code en modules distincts (configuration, modèles, routes, utilitaires), nous facilitons la maintenance et l'évolutivité du projet.
- **Modularité** : Chaque fichier et dossier a une responsabilité claire, ce qui permet d'ajouter ou de modifier des fonctionnalités sans affecter le reste du projet.
- **Facilité de Test** : En ayant un dossier dédié aux tests, nous encourageons les bonnes pratiques de tests automatisés.
- **Sécurité** : En utilisant des variables d'environnement pour les informations sensibles, nous évitons de les exposer directement dans le code source.
- **Lisibilité** : Une structure de projet claire et bien organisée améliore la lisibilité et facilite la prise en main par de nouveaux développeurs.

En suivant cette structure, nous assurons une base solide pour le développement d'applications Flask robustes et maintenables.
