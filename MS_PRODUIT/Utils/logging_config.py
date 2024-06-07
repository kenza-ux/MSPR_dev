# Utils/logging_config.py
import logging
import colorlog

def configure_logging():
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(levelname)s:%(name)s:%(message)s'))

    logger = colorlog.getLogger('flask_app')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger
