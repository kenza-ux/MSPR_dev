from flask_sqlalchemy import SQLAlchemy

# Initialiser l'extension SQLAlchemy
db = SQLAlchemy()

class Produit(db.Model):
    """
    Modèle de base de données pour la table Produits.

    Attributs:
        ProduitID (int): L'ID unique du produit.
        Nom (str): Le nom du produit.
        Description (str): La description du produit.
        Prix (float): Le prix du produit.
        Stock (int): Le stock du produit.
        Categorie (str): La catégorie du produit.
    """
    __tablename__ = 'Produits'
    
    ProduitID = db.Column(db.Integer, primary_key=True)
    Nom = db.Column(db.String(255))
    Description = db.Column(db.String(255))
    Prix = db.Column(db.Float)
    Stock = db.Column(db.Integer)
    Categorie = db.Column(db.String(255))

    def as_dict(self):
        """
        Convertit l'instance du modèle en dictionnaire.
        
        Retourne:
            dict: Une représentation dictionnaire de l'instance du modèle.
        """
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
