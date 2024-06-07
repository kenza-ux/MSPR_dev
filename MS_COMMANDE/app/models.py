from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Commande(db.Model):
    __tablename__ = 'Commandes'
    
    CommandeID = db.Column(db.Integer, primary_key=True)
    ClientID = db.Column(db.Integer)
    DateCommande = db.Column(db.String(255))
    Statut = db.Column(db.String(255))
    MontantTotal = db.Column(db.Float)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
