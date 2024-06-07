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
    'db': os.getenv('DB_NAME_cmd')
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
class Commande(db.Model):
    __tablename__ = 'Commandes'
    CommandeID = db.Column(db.Integer, primary_key=True)
    ClientID = db.Column(db.Integer)
    DateCommande = db.Column(db.String(255))
    Statut = db.Column(db.String(255))
    MontantTotal = db.Column(db.Float)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

@app.route('/commandes', methods=['GET'])
def get_commandes():
    try:
        commandes = Commande.query.all()
        app.logger.info("Fetched commandes list")
        return jsonify([commande.as_dict() for commande in commandes])
    except Exception as e:
        app.logger.error(f"Failed to fetch commandes: {e}")
        return make_response(jsonify({"error": "Internal Server Error"}), 500)

@app.route('/commandes/<int:id>', methods=['GET'])
def get_commande(id):
    try:
        commande = Commande.query.get(id)
        if commande:
            app.logger.info(f"Commande {id} found")
            return jsonify(commande.as_dict())
        else:
            app.logger.warning(f"Commande {id} not found")
            return make_response(jsonify({"error": "Commande not found"}), 404)
    except Exception as e:
        app.logger.error(f"Failed to fetch commande {id}: {e}")
        return make_response(jsonify({"error": "Internal Server Error"}), 500)

@app.route('/commandes', methods=['POST'])
def create_commande():
    if not request.json or not 'ClientID' in request.json or not 'DateCommande' in request.json or not 'MontantTotal' in request.json:
        app.logger.warning("Bad request: Missing required fields")
        return make_response(jsonify({"error": "Bad request"}), 400)
    try:
        commande = Commande(
            ClientID=request.json['ClientID'],
            DateCommande=request.json['DateCommande'],
            Statut=request.json.get('Statut', 'En cours'),
            MontantTotal=request.json['MontantTotal']
        )
        db.session.add(commande)
        db.session.commit()
        app.logger.info("Created new commande")
        return make_response(jsonify(commande.as_dict()), 201)
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Failed to create commande: {e}")
        return make_response(jsonify({"error": "Internal Server Error"}), 500)

@app.route('/commandes/<int:id>', methods=['PUT'])
def update_commande(id):
    try:
        commande = Commande.query.get(id)
        if not commande:
            app.logger.warning(f"Commande {id} not found for update")
            return make_response(jsonify({"error": "Commande not found"}), 404)
        
        data = request.json
        for key, value in data.items():
            setattr(commande, key, value)
        
        db.session.commit()
        app.logger.info(f"Updated commande {id}")
        return jsonify({"success": "Commande updated"})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Failed to update commande {id}: {e}")
        return make_response(jsonify({"error": "Internal Server Error"}), 500)

@app.route('/commandes/<int:id>', methods=['DELETE'])
def delete_commande(id):
    try:
        commande = Commande.query.get(id)
        if not commande:
            app.logger.warning(f"Commande {id} not found for deletion")
            return make_response(jsonify({"error": "Commande not found"}), 404)
        
        db.session.delete(commande)
        db.session.commit()
        app.logger.info(f"Deleted commande {id}")
        return jsonify({"success": "Commande deleted"})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Failed to delete commande {id}: {e}")
        return make_response(jsonify({"error": "Internal Server Error"}), 500)

if __name__ == '__main__':
    app.run()
