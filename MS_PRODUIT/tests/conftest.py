import pytest
from app.app import create_app
from app.models import db, Produit
from config import TestConfig

@pytest.fixture(scope='function')
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def test_client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def init_database(app):
    with app.app_context():
        # Supprimer tous les enregistrements existants pour éviter les conflits
        db.session.query(Produit).delete()
        db.session.commit()
        
        # Création des données initiales pour les tests
        produit1 = Produit(Nom='Produit Test', Description='Description Test', Prix=10.0, Stock=100, Categorie='Catégorie Test')
        db.session.add(produit1)
        db.session.commit()
        yield
        db.session.remove()
        db.drop_all()
