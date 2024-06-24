# test_routes.py

def test_get_commandes(test_client, init_database):
    response = test_client.get('/commandes')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['ClientID'] == 1

def test_get_commande(test_client, init_database):
    response = test_client.get('/commandes/1')
    assert response.status_code == 200
    assert response.json['ClientID'] == 1

def test_get_commande_not_found(test_client, init_database):
    response = test_client.get('/commandes/99')
    assert response.status_code == 404

def test_create_commande(test_client):
    new_commande = {
        'ClientID': 2,
        'DateCommande': '2023-02-01',
        'MontantTotal': 200.0
    }
    response = test_client.post('/commandes', json=new_commande)
    assert response.status_code == 201
    assert response.json['ClientID'] == 2

def test_create_commande_invalid(test_client):
    invalid_commande = {
        'ClientID': 3,
        'DateCommande': '2023-03-01'
        # MontantTotal manquant
    }
    response = test_client.post('/commandes', json=invalid_commande)
    assert response.status_code == 400

def test_update_commande(test_client, init_database):
    update_data = {
        'Statut': 'Livrée'
    }
    response = test_client.put('/commandes/1', json=update_data)
    assert response.status_code == 200
    assert response.json['success'] == 'Commande mise à jour'

def test_update_commande_not_found(test_client):
    update_data = {
        'Statut': 'Annulée'
    }
    response = test_client.put('/commandes/99', json=update_data)
    assert response.status_code == 404

def test_delete_commande(test_client, init_database):
    response = test_client.delete('/commandes/1')
    assert response.status_code == 200
    assert response.json['success'] == 'Commande supprimée'

def test_delete_commande_not_found(test_client):
    response = test_client.delete('/commandes/99')
    assert response.status_code == 404
