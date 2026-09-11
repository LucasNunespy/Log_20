import bcrypt
import jwt

from datetime import datetime, timedelta, timezone
from flask import current_app
from models.usuario import Usuario



def autenticar_usuario(email, senha):

    usuario = Usuario.query.filter_by(email=email).first()

    if usuario is None:
        return None

    if not usuario.ativo:
        return None

    senha_correta = bcrypt.checkpw(
        senha.encode("utf-8"),
        usuario.senha_hash.encode("utf-8")
    )

    if not senha_correta:
        return None

    return usuario


def gerar_access_token(usuario):

    payload = {
        "usuario_id": usuario.id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    token = jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return token

def gerar_refresh_token(usuario):

    payload = {
        "usuario_id": usuario.id,
        "tipo": "refresh",
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    }

    token = jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return token

def validar_refresh_token(token):

    try:
        payload = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )

        if payload.get("tipo") != "refresh":
            return None

        return payload

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None