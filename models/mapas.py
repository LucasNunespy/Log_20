from database.db import db


class Mapa(db.Model):
    __tablename__ = "mapas"

    id = db.Column(db.Integer, primary_key=True)
    numero_mapa = db.Column(db.String(50), nullable=False)
    data_operacao = db.Column(db.Date, nullable=False)
    motorista_id = db.Column(
        db.Integer,
        db.ForeignKey("motoristas.id"),
        nullable=False
    )
    km_previsto = db.Column(db.Numeric(10, 2), nullable=False)

    motorista = db.relationship(
    "Motorista",
    back_populates="mapas"
  ) 

    entregas = db.relationship(
        "Entrega",
        back_populates="mapa"
      ) 