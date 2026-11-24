
from database.db import db


class Jornada2ART(db.Model):
    __tablename__ = "jornadas_2art"

    id = db.Column(db.Integer, primary_key=True)
    matricula_motorista = db.Column(db.String(20), nullable=False)
    data_operacao = db.Column(db.Date, nullable=False)
    hora_matinal = db.Column(db.Time, nullable=True)
    limite_retorno = db.Column(db.DateTime, nullable=True)
    entrada_cdd = db.Column(db.DateTime, nullable=True)
    perda_jornada = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    mapas = db.relationship(
        "Jornada2ARTMapa",
        back_populates="jornada"
    )


class Jornada2ARTMapa(db.Model):
    __tablename__ = "jornadas_2art_mapas"

    id = db.Column(db.Integer, primary_key=True)

    jornada_id = db.Column(
        db.Integer,
        db.ForeignKey("jornadas_2art.id"),
        nullable=False
    )

    numero_mapa = db.Column(db.String(50), nullable=False)

    jornada = db.relationship(
        "Jornada2ART",
        back_populates="mapas"
    )
