from flask import Flask
from sqlalchemy import text
from config import Config
from app.models import db
from app.routes import routes
from app.utils.logging_config import configure_logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    logger = configure_logging()
    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)

    db.init_app(app)

    app.register_blueprint(routes)

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
