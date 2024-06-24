from flask import Blueprint, request, jsonify, make_response
from .models import db, Produit

routes = Blueprint('routes', __name__)

@routes.route('/produits', methods=['GET'])
def get_produits():
    try:
        produits = Produit.query.all()
        return jsonify([produit.as_dict() for produit in produits])
    except Exception as e:
        print(f"Erreur lors de la récupération des produits: {e}")
        return make_response(jsonify({"error": "Erreur interne du serveur"}), 500)

@routes.route('/produits/<int:id>', methods=['GET'])
def get_produit(id):
    try:
        produit = db.session.get(Produit, id)
        if produit:
            return jsonify(produit.as_dict())
        else:
            return make_response(jsonify({"error": "Produit non trouvé"}), 404)
    except Exception as e:
        print(f"Erreur lors de la récupération du produit {id}: {e}")
        return make_response(jsonify({"error": "Erreur interne du serveur"}), 500)

@routes.route('/produits', methods=['POST'])
def create_produit():
    if not request.json or not 'Nom' in request.json or not 'Prix' in request.json or not 'Stock' in request.json:
        return make_response(jsonify({"error": "Requête incorrecte"}), 400)
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
        return make_response(jsonify(produit.as_dict()), 201)
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la création du produit: {e}")
        return make_response(jsonify({"error": "Erreur interne du serveur"}), 500)

@routes.route('/produits/<int:id>', methods=['PUT'])
def update_produit(id):
    try:
        produit = db.session.get(Produit, id)
        if not produit:
            return make_response(jsonify({"error": "Produit non trouvé"}), 404)
        
        data = request.json
        for key, value in data.items():
            setattr(produit, key, value)
        
        db.session.commit()
        return jsonify({"success": "Produit mis à jour"})
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la mise à jour du produit {id}: {e}")
        return make_response(jsonify({"error": "Erreur interne du serveur"}), 500)

@routes.route('/produits/<int:id>', methods=['DELETE'])
def delete_produit(id):
    try:
        produit = db.session.get(Produit, id)
        if not produit:
            return make_response(jsonify({"error": "Produit non trouvé"}), 404)
        
        db.session.delete(produit)
        db.session.commit()
        return jsonify({"success": "Produit supprimé"})
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la suppression du produit {id}: {e}")
        return make_response(jsonify({"error": "Erreur interne du serveur"}), 500)
