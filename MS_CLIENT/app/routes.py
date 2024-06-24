from flask import Blueprint, request, jsonify, make_response
from .models import db, Client

routes = Blueprint('routes', 'routes')

@routes.route('/customers', methods=['GET'])
def get_customers():
    try:
        customers = Client.query.all()
        return jsonify([customer.as_dict() for customer in customers])
    except Exception as e:
        print(f"Erreur lors de la récupération des clients: {e}")
        return make_response(jsonify({"error": "Erreur interne du serveur"}), 500)

@routes.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    try:
        customer = db.session.get(Client, id)
        if customer:
            return jsonify(customer.as_dict())
        else:
            return make_response(jsonify({"error": "Client non trouvé"}), 404)
    except Exception as e:
        print(f"Erreur lors de la récupération du client {id}: {e}")
        return make_response(jsonify({"error": "Erreur interne du serveur"}), 500)

@routes.route('/customers', methods=['POST'])
def create_customer():
    if not request.json or not 'Email' in request.json:
        return make_response(jsonify({"error": "Requête incorrecte"}), 400)
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
        return make_response(jsonify(customer.as_dict()), 201)
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la création du client: {e}")
        return make_response(jsonify({"error": "Erreur interne du serveur"}), 500)

@routes.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    try:
        customer = db.session.get(Client, id)
        if not customer:
            return make_response(jsonify({"error": "Client non trouvé"}), 404)
        
        data = request.json
        for key, value in data.items():
            setattr(customer, key, value)
        
        db.session.commit()
        return jsonify({"success": "Client mis à jour"})
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la mise à jour du client {id}: {e}")
        return make_response(jsonify({"error": "Erreur interne du serveur"}), 500)

@routes.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    try:
        customer = db.session.get(Client, id)
        if not customer:
            return make_response(jsonify({"error": "Client non trouvé"}), 404)
        
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"success": "Client supprimé"})
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la suppression du client {id}: {e}")
        return make_response(jsonify({"error": "Erreur interne du serveur"}), 500)
