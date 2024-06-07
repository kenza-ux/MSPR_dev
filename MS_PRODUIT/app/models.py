from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Produit(db.Model):
    __tablename__ = 'Produits'
    
    ProduitID = db.Column(db.Integer, primary_key=True)
    Nom = db.Column(db.String(255))
    Description = db.Column(db.String(255))
    Prix = db.Column(db.Float)
    Stock = db.Column(db.Integer)
    Categorie = db.Column(db.String(255))

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
