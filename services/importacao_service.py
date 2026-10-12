
import csv
import io
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from database.db import db
from models.motoristas import Motorista
from models.mapas import Mapa
from models.entregas import Entrega


def converter_volume(valor):
    numero = Decimal(valor or "0")

    return numero.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )


def processar_csv(arquivo):

    conteudo = io.TextIOWrapper(
        arquivo.stream,
        encoding="utf-8-sig"
    )

    leitor = csv.DictReader(conteudo, delimiter=";")

    registros = list(leitor)

    if not registros:
        raise ValueError("O arquivo CSV está vazio.")

    mapas_csv = {}

    # Organiza os registros pelo mapa e pela data
    for linha in registros:

        numero_mapa = linha["tour_display_id"].strip()
        data_operacao = date.fromisoformat(linha["tour_date"].strip())
        nome_motorista = linha["driver_name"].strip()

        chave = (numero_mapa, data_operacao)

        if chave not in mapas_csv:
            mapas_csv[chave] = {
                "motorista": nome_motorista,
                "entregas": []
            }

        elif mapas_csv[chave]["motorista"] != nome_motorista:
            raise ValueError(
                f"Mapa {numero_mapa} possui motoristas diferentes no CSV."
            )

        mapas_csv[chave]["entregas"].append(linha)

    mapas_importados = 0
    entregas_importadas = 0
    mapas_ignorados = 0

    try:

        for (numero_mapa, data_operacao), dados in mapas_csv.items():

            # Verifica se o mapa já foi importado
            mapa_existente = Mapa.query.filter_by(
                numero_mapa=numero_mapa,
                data_operacao=data_operacao
            ).first()

            if mapa_existente:
                mapas_ignorados += 1
                continue

            # Busca o motorista cadastrado
            motorista = Motorista.query.filter_by(
                nome=dados["motorista"]
            ).first()

            if motorista is None:
                raise ValueError(
                    f"Motorista não cadastrado: {dados['motorista']}"
                )

            # Cria o mapa
            mapa = Mapa(
                numero_mapa=numero_mapa,
                data_operacao=data_operacao,
                motorista_id=motorista.id,
                km_previsto=None
            )

            db.session.add(mapa)

            # Cria as entregas vinculadas ao mapa
            for linha in dados["entregas"]:

                status = linha["status"].strip()

                motivo = None

                if status != "CONCLUDED":
                    motivo = (
                        linha["last_reason_waiting_modulation"].strip()
                        or linha["last_reason_rescheduled"].strip()
                        or None
                    )

                entrega = Entrega(
                    pdv_codigo=linha["poc_external_id"].strip(),
                    pdv_nome=linha["poc_name"].strip(),
                    status=status,
                    volume_entregue=converter_volume(
                        linha["total_delivered_vol"]
                    ),
                    volume_devolvido=converter_volume(
                        linha["total_refused_vol"]
                    ),
                    motivo_devolucao=motivo
                )

                mapa.entregas.append(entrega)

                entregas_importadas += 1

            mapas_importados += 1

        # Confirma a gravação de todos os registros
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return {
        "mapas": mapas_importados,
        "entregas": entregas_importadas,
        "ignorados": mapas_ignorados
    }
