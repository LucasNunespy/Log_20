from flask import Blueprint, render_template, request, jsonify


motoristas = Blueprint("motoristas", __name__)


@motoristas.route("/motoristas")
def pagina_motoristas():
    return render_template("motoristas.html")


@motoristas.route("/api/motoristas", methods=["POST"])
def cadastrar_motorista():

    dados = request.get_json()

    return jsonify(dados), 200

@motoristas.route("/api/motoristas", methods=["GET"])
def listar_motoristas():
    return jsonify([]), 200


@motoristas.route("/api/motoristas/<int:id>", methods=["GET"])
def buscar_motorista(id):
    return jsonify({"id": id}), 200


@motoristas.route("/api/motoristas/<int:id>", methods=["PUT"])
def atualizar_motorista(id):
    dados = request.get_json()

    return jsonify({
        "id": id,
        "dados": dados
    }), 200


@motoristas.route("/api/motoristas/<int:id>/status", methods=["PATCH"])
def alterar_status_motorista(id):
    dados = request.get_json()

    return jsonify({
        "id": id,
        "dados": dados
    }), 200