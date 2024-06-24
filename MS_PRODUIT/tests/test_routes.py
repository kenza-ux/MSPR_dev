import json

def test_get_produits(test_client, init_database):
    response = test_client.get('/produits')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['Nom'] == 'Produit Test'

def test_get_produit(test_client, init_database):
    response = test_client.get('/produits/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['Nom'] == 'Produit Test'

def test_get_produit_not_found(test_client, init_database):
    response = test_client.get('/produits/99')
    assert response.status_code == 404

def test_create_produit(test_client):
    new_produit = {
        'Nom': 'Nouveau Produit',
        'Description': 'Nouvelle Description',
        'Prix': 20.0,
        'Stock': 50,
        'Categorie': 'Nouvelle Catégorie'
    }
    response = test_client.post('/produits', json=new_produit)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['Nom'] == 'Nouveau Produit'

def test_create_produit_invalid(test_client):
    new_produit = {
        'Nom': 'Nouveau Produit',
    }
    response = test_client.post('/produits', json=new_produit)
    assert response.status_code == 400

def test_update_produit(test_client, init_database):
    update_data = {
        'Nom': 'Produit Mis à Jour',
        'Description': 'Description Mise à Jour',
        'Prix': 30.0,
        'Stock': 80,
        'Categorie': 'Catégorie Mise à Jour'
    }
    response = test_client.put('/produits/1', json=update_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == 'Produit mis à jour'

def test_update_produit_not_found(test_client, init_database):
    update_data = {
        'Nom': 'Produit Mis à Jour',
        'Description': 'Description Mise à Jour',
        'Prix': 30.0,
        'Stock': 80,
        'Categorie': 'Catégorie Mise à Jour'
    }
    response = test_client.put('/produits/99', json=update_data)
    assert response.status_code == 404

def test_delete_produit(test_client, init_database):
    response = test_client.delete('/produits/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == 'Produit supprimé'

def test_delete_produit_not_found(test_client, init_database):
    response = test_client.delete('/produits/99')
    assert response.status_code == 404
