# app.py

from flask import Flask
from sqlalchemy import text
from config import Config
from app.models import db
from app.routes import routes
from app.Utils.logging_config import configure_logging

def create_app(config_class=Config):
    """
    Crée et configure l'application Flask.

    Args:
        config_class (class): La classe de configuration à utiliser.

    Retourne:
        app (Flask): L'application Flask configurée.
    """
    print("create_app function is being called")  # Ligne de débogage

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configuration du logger
    logger = configure_logging()
    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)

    # Initialisation de la base de données
    db.init_app(app)

    # Enregistrement des routes
    app.register_blueprint(routes)

    # Vérification de la connexion directe à la base de données
    with app.app_context():
        try:
            with db.engine.connect() as connection:
                result = connection.execute(text('SELECT 1')).fetchone()
                if result:
                    app.logger.info("Connexion directe à la base de données réussie")
                else:
                    app.logger.error("Échec de l'exécution de la requête de test")
        except Exception as e:
            app.logger.error(f"Échec de la connexion directe à la base de données: {e}")

    return app
