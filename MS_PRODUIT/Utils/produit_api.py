import os
import logging
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from logging_config import configure_logging
import urllib.parse

load_dotenv()

app = Flask(__name__)

# Configuration du logger
logger = configure_logging()

# Configure Flask's logger to use the same handler
app.logger.handlers = logger.handlers
app.logger.setLevel(logger.level)

# Configuration de la base de données
db_config = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'db': os.getenv('DB_NAME_prod')
}

# Encode password for SQLAlchemy URI
encoded_password = urllib.parse.quote_plus(db_config['password'])

# Configuration de la base de données avec SQLAlchemy
db_uri = (
    f"mysql+pymysql://{db_config['user']}:{encoded_password}"
    f"@{db_config['host']}:{db_config['port']}/{db_config['db']}"
)
app.logger.debug(f"Database URI: {db_uri}")
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Configuration de Flask pour utiliser FLASK_ENV depuis .env
flask_env = os.getenv('FLASK_ENV')
if flask_env:
    app.config['ENV'] = flask_env
    app.config['DEBUG'] = flask_env == 'development'

# Modèle de la base de données
class Produit(db.Model):
    __tablename__ = 'Produits'
    ProduitID = db.Column(db.Integer, primary_key=True)
    Nom = db.Column(db.String(255))
    Description = db.Column(db.String(255))
    Prix = db.Column(db.Float)
    Stock = db.Column(db.Integer)
    Categorie = db.Column(db.String(255))

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

@app.route('/produits', methods=['GET'])
def get_produits():
    try:
        produits = Produit.query.all()
        app.logger.info("Fetched produits list")
        return jsonify([produit.as_dict() for produit in produits])
    except Exception as e:
        app.logger.error(f"Failed to fetch produits: {e}")
        return make_response(jsonify({"error": "Internal Server Error"}), 500)

@app.route('/produits/<int:id>', methods=['GET'])
def get_produit(id):
    try:
        produit = Produit.query.get(id)
        if produit:
            app.logger.info(f"Produit {id} found")
            return jsonify(produit.as_dict())
        else:
            app.logger.warning(f"Produit {id} not found")
            return make_response(jsonify({"error": "Produit not found"}), 404)
    except Exception as e:
        app.logger.error(f"Failed to fetch produit {id}: {e}")
        return make_response(jsonify({"error": "Internal Server Error"}), 500)

@app.route('/produits', methods=['POST'])
def create_produit():
    if not request.json or not 'Nom' in request.json or not 'Prix' in request.json or not 'Stock' in request.json:
        app.logger.warning("Bad request: Missing required fields")
        return make_response(jsonify({"error": "Bad request"}), 400)
    try:
        produit = Produit(
            Nom=request.json['Nom'],
            Description=request.json.get('Description', ""),
            Prix=request.json['Prix'],
            Stock=request.json['Stock'],
            Categorie=request.json.get('Categorie', "")
        )
        db.session.add(produit)
        db.session.commit()
        app.logger.info("Created new produit")
        return make_response(jsonify(produit.as_dict()), 201)
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Failed to create produit: {e}")
        return make_response(jsonify({"error": "Internal Server Error"}), 500)

@app.route('/produits/<int:id>', methods=['PUT'])
def update_produit(id):
    try:
        produit = Produit.query.get(id)
        if not produit:
            app.logger.warning(f"Produit {id} not found for update")
            return make_response(jsonify({"error": "Produit not found"}), 404)
        
        data = request.json
        for key, value in data.items():
            setattr(produit, key, value)
        
        db.session.commit()
        app.logger.info(f"Updated produit {id}")
        return jsonify({"success": "Produit updated"})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Failed to update produit {id}: {e}")
        return make_response(jsonify({"error": "Internal Server Error"}), 500)

@app.route('/produits/<int:id>', methods=['DELETE'])
def delete_produit(id):
    try:
        produit = Produit.query.get(id)
        if not produit:
            app.logger.warning(f"Produit {id} not found for deletion")
            return make_response(jsonify({"error": "Produit not found"}), 404)
        
        db.session.delete(produit)
        db.session.commit()
        app.logger.info(f"Deleted produit {id}")
        return jsonify({"success": "Produit deleted"})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Failed to delete produit {id}: {e}")
        return make_response(jsonify({"error": "Internal Server Error"}), 500)

if __name__ == '__main__':
    app.run()
