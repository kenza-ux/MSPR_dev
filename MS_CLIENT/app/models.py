from flask_sqlalchemy import SQLAlchemy

# Initialiser l'extension SQLAlchemy
db = SQLAlchemy()

class Client(db.Model):
    """
    Modèle de base de données pour la table Clients.
    
    Attributs:
        ClientID (int): L'ID unique du client.
        Nom (str): Le nom du client.
        Prenom (str): Le prénom du client.
        Email (str): L'adresse email unique du client.
        Telephone (str): Le numéro de téléphone du client.
        Adresse (str): L'adresse du client.
        Ville (str): La ville du client.
        CodePostal (str): Le code postal du client.
        Pays (str): Le pays du client.
    """
    
    __tablename__ = 'Clients'
    
    ClientID = db.Column(db.Integer, primary_key=True)
    Nom = db.Column(db.String(255))
    Prenom = db.Column(db.String(255))
    Email = db.Column(db.String(255), unique=True)
    Telephone = db.Column(db.String(255))
    Adresse = db.Column(db.String(255))
    Ville = db.Column(db.String(255))
    CodePostal = db.Column(db.String(255))
    Pays = db.Column(db.String(255))

    def as_dict(self):
        """
        Convertit l'instance du modèle en dictionnaire.
        
        Retourne:
            dict: Une représentation dictionnaire de l'instance du modèle.
        """
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
