# conftest.py

import pytest
from app.app import create_app
from app.models import db, Client
from config import TestConfig

@pytest.fixture(scope='function')
def test_client():
    flask_app = create_app(TestConfig)
    flask_app.config['TESTING'] = True

    with flask_app.app_context():
        db.create_all()

    yield flask_app.test_client()

    with flask_app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def init_database(test_client):
    with test_client.application.app_context():
        # Supprimer tous les enregistrements existants pour éviter les conflits
        db.session.query(Client).delete()
        db.session.commit()
        
        # Création des données initiales pour les tests
        client1 = Client(Nom='Test', Prenom='Client', Email='testclient@example.com')
        db.session.add(client1)
        db.session.commit()
        yield
        db.session.remove()
        db.drop_all()
