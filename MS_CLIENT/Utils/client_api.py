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
    'db': os.getenv('DB_NAME_cl'),
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

@app.route('/customers', methods=['GET'])
@token_required
def get_customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Clients")
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(customers)

@app.route('/customers/<int:id>', methods=['GET'])
@token_required
def get_customer(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Clients WHERE ClientID = %s", (id,))
    customer = cursor.fetchone()
    cursor.close()
    conn.close()
    if customer:
        return jsonify(customer)
    else:
        return make_response(jsonify({"error": "Customer not found"}), 404)

@app.route('/customers', methods=['POST'])
@token_required
def create_customer():
    if not request.json or not 'email' in request.json:
        return make_response(jsonify({"error": "Bad request"}), 400)
    customer = {
        'Nom': request.json.get('Nom', ""),
        'Prenom': request.json.get('Prenom', ""),
        'Email': request.json['email'],
        'Telephone': request.json.get('Telephone', ""),
        'Adresse': request.json.get('Adresse', ""),
        'Ville': request.json.get('Ville', ""),
        'CodePostal': request.json.get('CodePostal', ""),
        'Pays': request.json.get('Pays', "")
    }
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Clients (Nom, Prenom, Email, Telephone, Adresse, Ville, CodePostal, Pays) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                   (customer['Nom'], customer['Prenom'], customer['Email'], customer['Telephone'], customer['Adresse'], customer['Ville'], customer['CodePostal'], customer['Pays']))
    conn.commit()
    cursor.close()
    conn.close()
    return make_response(jsonify(customer), 201)

@app.route('/customers/<int:id>', methods=['PUT'])
@token_required
def update_customer(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Clients WHERE ClientID = %s", (id,))
    customer = cursor.fetchone()
    if not customer:
        return make_response(jsonify({"error": "Customer not found"}), 404)
    data = request.json
    updates = []
    values = []
    for field in ['Nom', 'Prenom', 'Email', 'Telephone', 'Adresse', 'Ville', 'CodePostal', 'Pays']:
        if field in data:
            updates.append(f"{field} = %s")
            values.append(data[field])
    values.append(id)
    update_query = "UPDATE Clients SET " + ", ".join(updates) + " WHERE ClientID = %s"
    cursor.execute(update_query, values)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": "Customer updated"})

@app.route('/customers/<int:id>', methods=['DELETE'])
@token_required
def delete_customer(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Clients WHERE ClientID = %s", (id,))
    conn.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    conn.close()
    if affected_rows:
        return jsonify({"success": "Customer deleted"})
    else:
        return make_response(jsonify({"error": "Customer not found"}), 404)

if __name__ == '__main__':
    app.run(debug=True)
