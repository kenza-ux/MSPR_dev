from flask import Blueprint, request, jsonify, make_response
from .models import db, Commande

routes = Blueprint('routes', __name__)

@routes.route('/commandes', methods=['GET'])
def get_commandes():
    try:
        commandes = Commande.query.all()
        return jsonify([commande.as_dict() for commande in commandes])
    except Exception as e:
        print(f"Erreur lors de la récupération des commandes: {e}")
        return make_response(jsonify({"error": "Erreur interne du serveur"}), 500)

@routes.route('/commandes/<int:id>', methods=['GET'])
def get_commande(id):
    try:
        commande = Commande.query.get(id)
        if commande:
            return jsonify(commande.as_dict())
        else:
            return make_response(jsonify({"error": "Commande non trouvée"}), 404)
    except Exception as e:
        print(f"Erreur lors de la récupération de la commande {id}: {e}")
        return make_response(jsonify({"error": "Erreur interne du serveur"}), 500)

@routes.route('/commandes', methods=['POST'])
def create_commande():
    if not request.json or not 'ClientID' in request.json or not 'DateCommande' in request.json or not 'MontantTotal' in request.json:
        return make_response(jsonify({"error": "Requête incorrecte"}), 400)
    try:
        commande = Commande(
            ClientID=request.json['ClientID'],
            DateCommande=request.json['DateCommande'],
            Statut=request.json.get('Statut', 'En cours'),
            MontantTotal=request.json['MontantTotal']
        )
        db.session.add(commande)
        db.session.commit()
        return make_response(jsonify(commande.as_dict()), 201)
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la création de la commande: {e}")
        return make_response(jsonify({"error": "Erreur interne du serveur"}), 500)

@routes.route('/commandes/<int:id>', methods=['PUT'])
def update_commande(id):
    try:
        commande = Commande.query.get(id)
        if not commande:
            return make_response(jsonify({"error": "Commande non trouvée"}), 404)
        
        data = request.json
        for key, value in data.items():
            setattr(commande, key, value)
        
        db.session.commit()
        return jsonify({"success": "Commande mise à jour"})
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la mise à jour de la commande {id}: {e}")
        return make_response(jsonify({"error": "Erreur interne du serveur"}), 500)

@routes.route('/commandes/<int:id>', methods=['DELETE'])
def delete_commande(id):
    try:
        commande = Commande.query.get(id)
        if not commande:
            return make_response(jsonify({"error": "Commande non trouvée"}), 404)
        
        db.session.delete(commande)
        db.session.commit()
        return jsonify({"success": "Commande supprimée"})
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la suppression de la commande {id}: {e}")
        return make_response(jsonify({"error": "Erreur interne du serveur"}), 500)
