import os
import logging
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from logging_config import configure_logging
import pymysql
import urllib.parse

load_dotenv()

app = Flask(__name__)

# Configuration du logger
logger = configure_logging()

# Configure Flask's logger to use the same handler
app.logger.handlers = logger.handlers
app.logger.setLevel(logger.level)

# Configuration de la connexion à la base de données
db_config = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'db': os.getenv('DB_NAME_cl')
}

def get_db_connection():
    connection = pymysql.connect(**db_config)
    return connection

# Vérification de la connexion directe
try:
    conn = get_db_connection()
    app.logger.info("Direct database connection successful")
    conn.close()
except Exception as e:
    app.logger.error(f"Failed direct database connection: {e}")

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
class Client(db.Model):
    __tablename__ = 'Clients'
    ClientID = db.Column(db.Integer, primary_key=True)
    Nom = db.Column(db.String(255))
    Prenom = db.Column(db.String(255))
    Email = db.Column(db.String(255), unique=True)
    Telephone = db.Column(db.String(255))
    Adresse = db.Column(db.String(255))
    Ville = db.Column(db.String(255))
    CodePostal = db.Column(db.String(255))
    Pays = db.Column(db.String(255))

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

@app.route('/customers', methods=['GET'])
def get_customers():
    try:
        customers = Client.query.all()
        app.logger.info("Fetched customers list")
        return jsonify([customer.as_dict() for customer in customers])
    except Exception as e:
        app.logger.error(f"Failed to fetch customers: {e}")
        return make_response(jsonify({"error": "Internal Server Error"}), 500)

@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    try:
        customer = Client.query.get(id)
        if customer:
            app.logger.info(f"Customer {id} found")
            return jsonify(customer.as_dict())
        else:
            app.logger.warning(f"Customer {id} not found")
            return make_response(jsonify({"error": "Customer not found"}), 404)
    except Exception as e:
        app.logger.error(f"Failed to fetch customer {id}: {e}")
        return make_response(jsonify({"error": "Internal Server Error"}), 500)

@app.route('/customers', methods=['POST'])
def create_customer():
    if not request.json or not 'Email' in request.json:
        app.logger.warning("Bad request: Missing email")
        return make_response(jsonify({"error": "Bad request"}), 400)
    try:
        customer = Client(
            Nom=request.json.get('Nom', ""),
            Prenom=request.json.get('Prenom', ""),
            Email=request.json['Email'],
            Telephone=request.json.get('Telephone', ""),
            Adresse=request.json.get('Adresse', ""),
            Ville=request.json.get('Ville', ""),
            CodePostal=request.json.get('CodePostal', ""),
            Pays=request.json.get('Pays', "")
        )
        db.session.add(customer)
        db.session.commit()
        app.logger.info("Created new customer")
        return make_response(jsonify(customer.as_dict()), 201)
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Failed to create customer: {e}")
        return make_response(jsonify({"error": "Internal Server Error"}), 500)

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    try:
        customer = Client.query.get(id)
        if not customer:
            app.logger.warning(f"Customer {id} not found for update")
            return make_response(jsonify({"error": "Customer not found"}), 404)
        
        data = request.json
        for key, value in data.items():
            setattr(customer, key, value)
        
        db.session.commit()
        app.logger.info(f"Updated customer {id}")
        return jsonify({"success": "Customer updated"})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Failed to update customer {id}: {e}")
        return make_response(jsonify({"error": "Internal Server Error"}), 500)

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    try:
        customer = Client.query.get(id)
        if not customer:
            app.logger.warning(f"Customer {id} not found for deletion")
            return make_response(jsonify({"error": "Customer not found"}), 404)
        
        db.session.delete(customer)
        db.session.commit()
        app.logger.info(f"Deleted customer {id}")
        return jsonify({"success": "Customer deleted"})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Failed to delete customer {id}: {e}")
        return make_response(jsonify({"error": "Internal Server Error"}), 500)

if __name__ == '__main__':
    app.run()
