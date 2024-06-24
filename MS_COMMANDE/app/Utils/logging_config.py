# Utils/logging_config.py

import logging
import colorlog

def configure_logging():
    """
    Configure le logger pour l'application Flask avec un format coloré.

    Retourne:
        logger (logging.Logger): L'objet logger configuré.
    """
    # Crée un gestionnaire de flux avec un format coloré
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(levelname)s:%(name)s:%(message)s'
    ))

    # Obtient un logger avec le nom 'flask_app'
    logger = colorlog.getLogger('flask_app')
    # Ajoute le gestionnaire de flux au logger
    logger.addHandler(handler)
    # Définit le niveau de logging à DEBUG
    logger.setLevel(logging.DEBUG)

    return logger
