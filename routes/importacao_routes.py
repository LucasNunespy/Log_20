
from flask import Blueprint, render_template, request
from services.importacao_service import processar_csv


importacao = Blueprint("importacao", __name__)


@importacao.route("/importacao", methods=["GET", "POST"])
def pagina_importacao():

    if request.method == "POST":

        arquivo = request.files.get("arquivo")

        if arquivo is None or arquivo.filename == "":
            return "Nenhum arquivo selecionado", 400

        try:
            resultado = processar_csv(arquivo)

        except (ValueError, KeyError) as erro:
            return f"Erro na importação: {erro}", 400

        except Exception:
            return "Erro ao importar o arquivo. Verifique o terminal.", 500

        return (
            f"Importação concluída! "
            f"Mapas: {resultado['mapas']} | "
            f"Entregas: {resultado['entregas']} | "
            f"Mapas já existentes: {resultado['ignorados']}"
        ), 200

    return render_template("importacao.html")
