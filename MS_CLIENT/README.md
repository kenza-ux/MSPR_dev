# MS_CLIENT API 🚀

Ce projet est une API Flask pour gérer les clients. Suivez les instructions ci-dessous pour configurer l'environnement, installer les dépendances et démarrer l'API.

## Prérequis 🛠️

- Python 3.6 ou supérieur
- `pip` (gestionnaire de paquets pour Python)

## Configuration de l'Environnement 🌐

### Script Bash (Linux/Mac) 🐧🍏

1. Créer et activer un environnement virtuel, installer les dépendances et démarrer l'API en exécutant le script `setup.sh`.

```bash
./setup.sh
```

Si vous préférez les commandes manuelles, suivez les étapes ci-dessous :

1. Créer un environnement virtuel :

```bash
python -m venv env
```

2. Activer l'environnement virtuel :

```bash
source env/bin/activate
```

3. Installer les dépendances depuis requirements.txt :

```bash
pip install -r requirements.txt
```

4. Démarrer l'API Flask :

```bash
python run.py
```


### Script Bash (Linux/Mac) 🐧🍏

1. Créer et activer un environnement virtuel, installer les dépendances et démarrer l'API en exécutant le script `setup.bat`.

```bash
./setup.bat
```

Si vous préférez les commandes manuelles, suivez les étapes ci-dessous :

1. Créer un environnement virtuel :

```bash
python -m venv env
```

2. Activer l'environnement virtuel :

```bash
call env/bin/activate
```

3. Installer les dépendances depuis requirements.txt :

```bash
pip install -r requirements.txt
```

4. Démarrer l'API Flask :

```bash
python run.py
```


### Configuration des Variables d'Environnement 🌿

Assurez-vous de configurer un fichier .env à la racine du projet avec les variables suivantes :

```bash
DB_HOST=your_database_host
DB_PORT=your_database_port
DB_USER=your_database_user
DB_PASS=your_database_password
DB_NAME_cl=your_database_name
FLASK_ENV=development
```

### Utilisation de l'API 📬

Une fois l'API démarrée, elle sera accessible à l'adresse http://127.0.0.1:5000. Vous pouvez utiliser des outils comme curl ou Postman pour interagir avec l'API.

**Endpoints Disponibles 🔗**
- GET /customers : Récupérer la liste de tous les clients.
- GET /customers/<id> : Récupérer un client spécifique par ID.
- POST /customers : Créer un nouveau client.
- PUT /customers/<id> : Mettre à jour un client existant par ID.
- DELETE /customers/<id> : Supprimer un client existant par ID.
