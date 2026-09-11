from flask import Blueprint, render_template, request, make_response, redirect, url_for

from models.usuario import Usuario


from services.auth_service import autenticar_usuario, gerar_access_token, gerar_refresh_token, validar_refresh_token


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario = autenticar_usuario(email, senha)

        if usuario is None:
            return render_template(
                "auth/login.html",
                erro="E-mail ou senha inválidos"
            )

        access_token = gerar_access_token(usuario)
        refresh_token = gerar_refresh_token(usuario)

        response = make_response(
            redirect(url_for("index"))
        )

        response.set_cookie(
            "access_token",
            access_token,
            httponly=True,
            secure=False,
            samesite="Lax"
        )

        response.set_cookie(
            "refresh_token",
            refresh_token,
            httponly=True,
            secure=False,
            samesite="Lax"
        )

        return response

    return render_template("auth/login.html")



@auth.route("/refresh", methods=["POST"])
def refresh():

    refresh_token = request.cookies.get("refresh_token")

    if refresh_token is None:
        return "Refresh token não encontrado", 401

    payload = validar_refresh_token(refresh_token)

    if payload is None:
        return "Refresh token inválido ou expirado", 401

    usuario = Usuario.query.get(payload["usuario_id"])

    if usuario is None:
        return "Usuário não encontrado", 401

    novo_access_token = gerar_access_token(usuario)

    response = make_response("Access token renovado")

    response.set_cookie(
        "access_token",
        novo_access_token,
        httponly=True,
        secure=False,
        samesite="Lax"
    )

    return response


@auth.route("/logout")
def logout():

    response = make_response(
        redirect(url_for("auth.login"))
    )

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return response