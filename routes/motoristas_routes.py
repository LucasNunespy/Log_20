from flask import Blueprint, render_template, request, jsonify
from models.motoristas import Motorista
from database.db import db


motoristas = Blueprint("motoristas", __name__)


@motoristas.route("/motoristas")
def pagina_motoristas():
    return render_template("motoristas.html")




@motoristas.route("/api/motoristas", methods=["POST"])
def cadastrar_motorista():

    dados = request.get_json()

    if "matricula" not in dados or "nome" not in dados:
        return jsonify({
            "erro": "Matrícula e nome são obrigatórios"
        }), 400
    

    if not dados["matricula"] or not dados["nome"]:
        return jsonify({
            "erro": "Matrícula e nome não podem estar vazios"
        }), 400

    if not isinstance(dados["matricula"], str) or not isinstance(dados["nome"], str):
        return jsonify({
            "erro": "Matrícula e nome devem ser textos"
        }), 400
    

    try:
        motorista_existente = Motorista.query.filter_by(
            matricula=dados["matricula"]
        ).first()

    except Exception:
        return jsonify({
            "erro": "Erro ao verificar matrícula"
        }), 500


    if motorista_existente:
        return jsonify({
            "erro": "Matrícula já cadastrada"
        }), 409

    novo_motorista = Motorista(
        matricula=dados["matricula"],
        nome=dados["nome"]
    )   

    try:
        db.session.add(novo_motorista)
        db.session.commit()

    except Exception:
        db.session.rollback()

        return jsonify({
            "erro": "Erro ao cadastrar motorista"
        }), 500

    return jsonify({
    "mensagem": "Motorista cadastrado com sucesso"
    }), 201




@motoristas.route("/api/motoristas", methods=["GET"])
def listar_motoristas():

    try:
        lista_motoristas = Motorista.query.all()

    except Exception:
        return jsonify({
            "erro": "Erro ao buscar motoristas"
        }), 500


    resultado = []

    for motorista in lista_motoristas:
        resultado.append({
            "id": motorista.id,
            "matricula": motorista.matricula,
            "nome": motorista.nome,
            "ativo": motorista.ativo
        })

    return jsonify(resultado), 200




@motoristas.route("/api/motoristas/<int:id>", methods=["GET"])
def buscar_motorista(id):

    try:
        motorista = Motorista.query.get(id)

    except Exception:
        return jsonify({
            "erro": "Erro ao buscar motorista"
        }), 500
    

    if motorista is None:
        return jsonify({
            "erro": "Motorista não encontrado"
        }), 404

    return jsonify({
        "id": motorista.id,
        "matricula": motorista.matricula,
        "nome": motorista.nome,
        "ativo": motorista.ativo
    }), 200



@motoristas.route("/api/motoristas/<int:id>", methods=["PUT"])
def atualizar_motorista(id):

    try:
        motorista = Motorista.query.get(id)

    except Exception:
        return jsonify({
            "erro": "Erro ao buscar motorista"
        }), 500

    if motorista is None:
        return jsonify({
            "erro": "Motorista não encontrado"
        }), 404

    dados = request.get_json()

    if "matricula" not in dados or "nome" not in dados:
        return jsonify({
            "erro": "Matrícula e nome são obrigatórios"
        }), 400

    if not dados["matricula"] or not dados["nome"]:
        return jsonify({
            "erro": "Matrícula e nome não podem estar vazios"
        }), 400

    if not isinstance(dados["matricula"], str) or not isinstance(dados["nome"], str):
        return jsonify({
            "erro": "Matrícula e nome devem ser textos"
        }), 400

    try:
        motorista_existente = Motorista.query.filter_by(
            matricula=dados["matricula"]
        ).first()

    except Exception:
        return jsonify({
            "erro": "Erro ao verificar matrícula"
        }), 500

    if motorista_existente and motorista_existente.id != motorista.id:
        return jsonify({
            "erro": "Matrícula já cadastrada"
        }), 409

    motorista.matricula = dados["matricula"]
    motorista.nome = dados["nome"]

    try:
        db.session.commit()

    except Exception:
        db.session.rollback()

        return jsonify({
            "erro": "Erro ao atualizar motorista"
        }), 500

    return jsonify({
    "mensagem": "Motorista atualizado com sucesso"
}), 200




@motoristas.route("/api/motoristas/<int:id>/status", methods=["PATCH"])
def atualizar_status_motorista(id):

    try:
        motorista = Motorista.query.get(id)

    except Exception:
        return jsonify({
            "erro": "Erro ao buscar motorista"
        }), 500
    if motorista is None:
        return jsonify({
            "erro": "Motorista não encontrado"
        }), 404

    dados = request.get_json()

    if "ativo" not in dados:
        return jsonify({
            "erro": "Status ativo é obrigatório"
        }), 400

    if not isinstance(dados["ativo"], bool):
        return jsonify({
            "erro": "Status ativo deve ser verdadeiro ou falso"
        }), 400

    motorista.ativo = dados["ativo"]

    try:
        db.session.commit()

    except Exception:
        db.session.rollback()

        return jsonify({
            "erro": "Erro ao atualizar status do motorista"
        }), 500

    return jsonify({
        "mensagem": "Status do motorista atualizado com sucesso"
    }), 200