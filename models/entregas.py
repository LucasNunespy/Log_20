from database.db import db


class Entrega(db.Model):
    __tablename__ = "entregas"

    id = db.Column(db.Integer, primary_key=True)

    mapa_id = db.Column(
        db.Integer,
        db.ForeignKey("mapas.id"),
        nullable=False
    )

    pdv_codigo = db.Column(db.String(50), nullable=False)
    pdv_nome = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    volume_entregue = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=0
    )

    volume_devolvido = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=0
    )

    motivo_devolucao = db.Column(db.String(255), nullable=True)

    mapa = db.relationship(
    "Mapa",
    back_populates="entregas"
)