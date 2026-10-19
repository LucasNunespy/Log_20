from flask import Blueprint, jsonify, request
from services.operacao_service import consultar_resumo_operacao
from datetime import datetime

operacao = Blueprint("operacao", __name__)

@operacao.route("/api/operacao/resumo", methods=["GET"])
def resumo_operacao():
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    try:
        if data_inicio is not None:
            data_inicio = datetime.strptime(
                data_inicio, "%Y-%m-%d"
            ).date()

        if data_fim is not None:
            data_fim = datetime.strptime(
                data_fim, "%Y-%m-%d"
            ).date()

    except ValueError:
        return jsonify({
            "erro": "Data inválida. Utilize o formato AAAA-MM-DD."
        }), 400

    if data_inicio is not None and data_fim is not None:
        if data_inicio > data_fim:
            return jsonify({
                "erro": "A data inicial não pode ser posterior à data final."
            }), 400
    
    resumo = consultar_resumo_operacao(data_inicio, data_fim)

    return jsonify(resumo), 200