import os
from flask import Flask, request, jsonify, make_response
import pymysql
import pymysql.cursors

app = Flask(__name__)

# Configuration de la connexion à la base de données
db_config = {
    'host': os.getenv('DB_HOST'),
    'port': 3306,
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'db': os.getenv('DB_NAME_cmd'),

}

def get_db_connection():
    connection = pymysql.connect(**db_config)
    return connection

@app.route('/commandes', methods=['GET'])
def get_commandes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Commandes")
    commandes = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(commandes)

@app.route('/commandes/<int:id>', methods=['GET'])
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