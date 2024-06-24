from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Commande(db.Model):
    """
    Modèle de base de données pour la table Commandes.

    Attributs:
        CommandeID (int): L'ID unique de la commande.
        ClientID (int): L'ID unique du client.
        DateCommande (str): La date de la commande.
        Statut (str): Le statut de la commande.
        MontantTotal (float): Le montant total de la commande.
    """
    __tablename__ = 'Commandes'
    
    CommandeID = db.Column(db.Integer, primary_key=True)
    ClientID = db.Column(db.Integer)
    DateCommande = db.Column(db.String(255))
    Statut = db.Column(db.String(255))
    MontantTotal = db.Column(db.Float)

    def as_dict(self):
        """
        Convertit l'instance du modèle en dictionnaire.

        Retourne:
            dict: Une représentation dictionnaire de l'instance du modèle.
        """
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
