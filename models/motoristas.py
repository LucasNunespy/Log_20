from database.db import db

class Motorista(db.Model):
    __tablename__ = "motoristas"
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(20), nullable=False, unique=True)
    nome = db.Column(db.String(150), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    mapas = db.relationship(
    "Mapa",
    back_populates="motorista"
)
