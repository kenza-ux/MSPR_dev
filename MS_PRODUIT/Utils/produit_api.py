import os
import pymysql
from flask import Flask, request, jsonify, make_response
from dotenv import load_dotenv
import secrets
from functools import wraps

load_dotenv()

app = Flask(__name__)

# Configuration de la connexion à la base de données
db_config = {
    'host': os.getenv('DB_HOST'),
    'port': 3306,
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'db': os.getenv('DB_NAME_prod'),
}

db_config_user = {
    'host': os.getenv('DB_HOST'),
    'port': 3306,
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'db': os.getenv('DB_USERS'),
}

current_token = None

def generate_token():
    return secrets.token_urlsafe(32)

def get_db_connection_users():
    connection = pymysql.connect(**db_config_user)
    return connection

@app.route('/login', methods=['POST'])
def login():
    global current_token
    data = request.json

    if not data or not data.get('username') or not data.get('password'):
        return make_response(jsonify({"error": "Missing username or password"}), 400)

    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection_users()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        return make_response(jsonify({"error": "Invalid username or password"}), 401)

    current_token = generate_token()
    return jsonify({"token": current_token}), 200

def get_db_connection():
    connection = pymysql.connect(**db_config)
    return connection

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        global current_token
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return make_response(jsonify({"error": "Unauthorized"}), 401)

        received_token = token.split('Bearer ')[1]
        if received_token != current_token:
            return make_response(jsonify({"error": "Unauthorized"}), 401)

        return f(*args, **kwargs)
    return decorated_function

@app.route('/produits', methods=['GET']) # Get fonctionelle 
@token_required
def get_produits():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produits")
    produits = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(produits)

@app.route('/produits/<int:id>', methods=['GET']) # Get 
@token_required
def get_produit(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produits WHERE ProduitID = %s", (id,))
    produit = cursor.fetchone()
    cursor.close()
    conn.close()
    if produit:
        return jsonify(produit)
    else:
        return make_response(jsonify({"error": "Produit not found"}), 404)

@app.route('/produits', methods=['POST'])
@token_required
def create_produit():
    if not request.json or not 'Nom' in request.json or not 'Prix' in request.json or not 'Stock' in request.json:
        return make_response(jsonify({"error": "Bad request"}), 400)
    produit = {
        'Nom': request.json['Nom'],
        'Description': request.json.get('Description', ""),
        'Prix': request.json['Prix'],
        'Stock': request.json['Stock'],
        'Categorie': request.json.get('Categorie', "")
    }
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produits (Nom, Description, Prix, Stock, Categorie) VALUES (%s, %s, %s, %s, %s)",
                   (produit['Nom'], produit['Description'], produit['Prix'], produit['Stock'], produit['Categorie']))
    conn.commit()
    cursor.close()
    conn.close()
    return make_response(jsonify(produit), 201)

@app.route('/produits/<int:id>', methods=['PUT'])
@token_required
def update_produit(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produits WHERE ProduitID = %s", (id,))
    produit = cursor.fetchone()
    if not produit:
        return make_response(jsonify({"error": "Produit not found"}), 404)
    data = request.json
    updates = []
    for field in ['Nom', 'Description', 'Prix', 'Stock', 'Categorie']:
        if field in data:
            updates.append(f"{field} = %s")
    update_query = "UPDATE produits SET " + ", ".join(updates) + " WHERE ProduitID = %s"
    cursor.execute(update_query, [data[field] for field in data if field in updates] + [id])
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": "Produit updated"})

@app.route('/produits/<int:id>', methods=['DELETE'])
@token_required
def delete_produit(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produits WHERE ProduitID = %s", (id,))
    conn.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    conn.close()
    if affected_rows:
        return jsonify({"success": "Produit deleted"})
    else:
        return make_response(jsonify({"error": "Produit not found"}), 404)

if __name__ == '__main__':
    app.run(debug=True)


