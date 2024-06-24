import pytest
from app.models import Client, db

def test_get_customers(test_client, init_database):
    response = test_client.get('/customers')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['Nom'] == 'Test'
    assert data[0]['Email'] == 'testclient@example.com'

def test_get_customer(test_client, init_database):
    response = test_client.get('/customers/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['Nom'] == 'Test'
    assert data['Email'] == 'testclient@example.com'

def test_get_customer_not_found(test_client):
    response = test_client.get('/customers/99')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Client non trouvé'

def test_create_customer(test_client):
    new_customer = {
        'Nom': 'Nouveau',
        'Prenom': 'Client',
        'Email': 'nouveauclient@example.com'
    }
    response = test_client.post('/customers', json=new_customer)
    assert response.status_code == 201
    data = response.get_json()
    assert data['Nom'] == 'Nouveau'
    assert data['Email'] == 'nouveauclient@example.com'

def test_create_customer_invalid(test_client):
    new_customer = {
        'Nom': 'Nouveau',
        'Prenom': 'Client'
        # Email is missing
    }
    response = test_client.post('/customers', json=new_customer)
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Requête incorrecte'

def test_update_customer(test_client, init_database):
    update_data = {
        'Nom': 'Updated',
        'Prenom': 'Client',
        'Email': 'updatedclient@example.com'
    }
    response = test_client.put('/customers/1', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == 'Client mis à jour'

def test_update_customer_not_found(test_client):
    update_data = {
        'Nom': 'Updated',
        'Prenom': 'Client',
        'Email': 'updatedclient@example.com'
    }
    response = test_client.put('/customers/99', json=update_data)
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Client non trouvé'

def test_delete_customer(test_client, init_database):
    response = test_client.delete('/customers/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == 'Client supprimé'

def test_delete_customer_not_found(test_client):
    response = test_client.delete('/customers/99')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Client non trouvé'
