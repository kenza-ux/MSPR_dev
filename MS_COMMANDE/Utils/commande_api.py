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
    'db': os.getenv('DB_NAME_cmd'),
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


@app.route('/commandes', methods=['GET'])
@token_required
def get_commandes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Commandes")
    commandes = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(commandes)

@app.route('/commandes/<int:id>', methods=['GET'])
@token_required
def get_commande(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Commandes WHERE CommandeID = %s", (id,))
    commande = cursor.fetchone()
    cursor.close()
    conn.close()
    if commande:
        return jsonify(commande)
    else:
        return make_response(jsonify({"error": "Commande not found"}), 404)

@app.route('/commandes', methods=['POST'])
@token_required

def create_commande():
    if not request.json or not 'ClientID' in request.json or not 'DateCommande' in request.json or not 'MontantTotal' in request.json:
        return make_response(jsonify({"error": "Bad request"}), 400)
    commande = {
        'ClientID': request.json['ClientID'],
        'DateCommande': request.json['DateCommande'],
        'Statut': request.json.get('Statut', 'En cours'),
        'MontantTotal': request.json['MontantTotal']
    }
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Commandes (ClientID, DateCommande, Statut, MontantTotal) VALUES (%s, %s, %s, %s)",
                   (commande['ClientID'], commande['DateCommande'], commande['Statut'], commande['MontantTotal']))
    conn.commit()
    cursor.close()
    conn.close()
    return make_response(jsonify(commande), 201)

@app.route('/commandes/<int:id>', methods=['PUT'])
@token_required

def update_commande(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Commandes WHERE CommandeID = %s", (id,))
    commande = cursor.fetchone()
    if not commande:
        return make_response(jsonify({"error": "Commande not found"}), 404)
    data = request.json
    print("here", data)
    updates = []
    values = []

    for field in ['ClientID', 'DateCommande', 'Statut', 'MontantTotal']:
        if field in data:
            updates.append(f"{field} = %s")
            values.append(data[field])
    values.append(id)
    update_query = "UPDATE Commandes SET " + ", ".join(updates) + " WHERE CommandeID = %s"
    print("update final",update_query)
    cursor.execute(update_query, values)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": "Commande updated"})

@app.route('/commandes/<int:id>', methods=['DELETE'])
@token_required

def delete_commande(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Commandes WHERE CommandeID = %s", (id,))
    conn.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    conn.close()
    if affected_rows:
        return jsonify({"success": "Commande deleted"})
    else:
        return make_response(jsonify({"error": "Commande not found"}), 404)


# penser à faire la méthode patch afin d'éviter d'écraser tous les id semblale à celui que je veux avec les modifs d'une seule commandes
if __name__ == '__main__':
    app.run(debug=True)




