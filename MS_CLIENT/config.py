import os
from dotenv import load_dotenv
import urllib.parse

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

class Config:
    """
    Classe de configuration pour l'application Flask.
    Les configurations sont chargées depuis les variables d'environnement.
    """
    
    # Charger les informations de connexion à la base de données depuis les variables d'environnement
    DB_USER = os.getenv('DB_USER')
    DB_PASS = urllib.parse.quote_plus(os.getenv('DB_PASS'))  # Encoder le mot de passe pour l'URI
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT', 3306)
    DB_NAME = os.getenv('DB_NAME_cl')

    # Construire l'URI de la base de données pour SQLAlchemy
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    
    # Désactiver le suivi des modifications de SQLAlchemy pour des raisons de performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Charger l'environnement de Flask depuis les variables d'environnement
    ENV = os.getenv('FLASK_ENV')
    DEBUG = ENV == 'development'  # Activer le mode débogage si l'environnement est en développement
