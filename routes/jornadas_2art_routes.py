
from flask import Blueprint, request
from services.jornadas_2art_service import processar_csv_2art


jornadas_2art = Blueprint("jornadas_2art", __name__)


@jornadas_2art.route("/api/jornadas-2art/importar", methods=["POST"])
def importar_jornadas_2art():

    arquivo = request.files.get("arquivo")

    if arquivo is None or arquivo.filename == "":
        return "Nenhum arquivo selecionado", 400

    try:
        resultado = processar_csv_2art(arquivo)

    except (ValueError, KeyError) as erro:
        return f"Erro na importação: {erro}", 400

    except Exception:
        return "Erro ao importar o arquivo. Verifique o terminal.", 500

    return (
        f"Importação concluída! "
        f"Jornadas: {resultado['jornadas']} | "
        f"Mapas: {resultado['mapas']} | "
        f"Jornadas já existentes: {resultado['ignoradas']}"
    ), 200
