# from flask import Flask
# from sqlalchemy import text
# from config import Config
# from app.models import db
# from app.routes import routes
# from app.Utils.logging_config import configure_logging

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     # Configuration du logger
#     logger = configure_logging()
#     app.logger.handlers = logger.handlers
#     app.logger.setLevel(logger.level)

#     # Initialisation de la base de données
#     db.init_app(app)

#     # Enregistrement des routes
#     app.register_blueprint(routes)

#     # Vérification de la connexion directe
#     with app.app_context():
#         try:
#             with db.engine.connect() as connection:
#                 result = connection.execute(text('SELECT 1')).fetchone()
#                 if result:
#                     app.logger.info("Direct database connection successful")
#                 else:
#                     app.logger.error("Failed to execute test query")
#         except Exception as e:
#             app.logger.error(f"Failed direct database connection: {e}")

#     return app
