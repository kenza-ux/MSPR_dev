import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

class Config:
    DB_USER = os.getenv('DB_USER')
    DB_PASS = urllib.parse.quote_plus(os.getenv('DB_PASS'))
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT', 3306)
    DB_NAME = os.getenv('DB_NAME_prod')

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = os.getenv('FLASK_ENV')
    DEBUG = ENV == 'development'
