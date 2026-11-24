import csv
import io
from datetime import datetime, timedelta

from database.db import db
from models.jornadas_2art import Jornada2ART, Jornada2ARTMapa


def processar_csv_2art(arquivo):

    conteudo = io.TextIOWrapper(
        arquivo.stream,
        encoding="cp1252"
    )

    leitor = csv.DictReader(conteudo, delimiter=";")
    registros = list(leitor)

    if not registros:
        raise ValueError("O arquivo CSV 2ART está vazio.")

    jornadas_csv = {}

    # 1. Leitura e organização dos registros
    for linha in registros:

        matricula = (linha["MatricMotorista"] or "").strip()

        # Ignora cabeçalhos repetidos e marcador final do arquivo
        if matricula == "MatricMotorista":
            continue

        if not matricula and linha["Data"] == "\x1a":
            continue

        data_operacao = datetime.strptime(
            linha["Data"].strip(),
            "%d%m%Y"
        ).date()

        numero_mapa = linha["Mapa"].strip()

        # Ignora registros sem jornada prevista
        if (
            linha["HrMatinal"].strip() == "00:00"
            and linha["HrMetaJornada"].strip() == "00000"
        ):
            continue

        hora_matinal = datetime.strptime(
            linha["HrMatinal"].strip(),
            "%H:%M"
        ).time()

        meta_jornada = datetime.strptime(
            linha["HrMetaJornada"].strip(),
            "%H:%M"
        ).time()

        entrada_cdd = (linha["HrEntr"] or "").strip()

        if entrada_cdd:
            entrada_cdd = datetime.strptime(
                entrada_cdd,
                "%d/%m/%Y %H:%M"
            )
        else:
            entrada_cdd = None

        # 2. Cálculo do limite de retorno
        inicio_jornada = datetime.combine(
            data_operacao,
            hora_matinal
        )

        duracao_jornada = timedelta(
            hours=meta_jornada.hour,
            minutes=meta_jornada.minute
        )

        limite_retorno = inicio_jornada + duracao_jornada

        # Desconsidera retornos anteriores à operação
        if entrada_cdd is not None:
            if entrada_cdd.date() < data_operacao:
                entrada_cdd = None

        # 3. Agrupamento por motorista e data
        chave = (matricula, data_operacao)

        if chave not in jornadas_csv:

            jornadas_csv[chave] = {
                "mapas": [],
                "hora_matinal": hora_matinal,
                "limite_retorno": limite_retorno,
                "entrada_cdd": entrada_cdd
            }

        else:
            dados = jornadas_csv[chave]

            # Confere os horários previstos
            if (
                dados["hora_matinal"] != hora_matinal
                or dados["limite_retorno"] != limite_retorno
            ):
                raise ValueError(
                    f"Horários divergentes para motorista {matricula}"
                )

            # Mantém o último retorno válido
            retorno_atual = dados["entrada_cdd"]

            if entrada_cdd is not None:
                if retorno_atual is None or entrada_cdd > retorno_atual:
                    dados["entrada_cdd"] = entrada_cdd

        if numero_mapa not in jornadas_csv[chave]["mapas"]:
            jornadas_csv[chave]["mapas"].append(numero_mapa)

    # 4. Gravação no MySQL
    jornadas_importadas = 0
    mapas_importados = 0
    jornadas_ignoradas = 0

    try:

        for (matricula, data_operacao), dados in jornadas_csv.items():

            # Verifica se a jornada já existe
            jornada_existente = Jornada2ART.query.filter_by(
                matricula_motorista=matricula,
                data_operacao=data_operacao
            ).first()

            if jornada_existente:
                jornadas_ignoradas += 1
                continue

            # 5. Identifica a perda de jornada
            entrada_cdd = dados["entrada_cdd"]
            limite_retorno = dados["limite_retorno"]

            perda_jornada = False

            if entrada_cdd is not None:
                if entrada_cdd > limite_retorno:
                    perda_jornada = True

            # 6. Cria a jornada
            jornada = Jornada2ART(
                matricula_motorista=matricula,
                data_operacao=data_operacao,
                hora_matinal=dados["hora_matinal"],
                limite_retorno=limite_retorno,
                entrada_cdd=entrada_cdd,
                perda_jornada=perda_jornada
            )

            db.session.add(jornada)

            # 7. Associa os mapas à jornada
            for numero_mapa in dados["mapas"]:

                mapa = Jornada2ARTMapa(
                    numero_mapa=numero_mapa
                )

                jornada.mapas.append(mapa)
                mapas_importados += 1

            jornadas_importadas += 1

        # 8. Confirma a gravação
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return {
        "jornadas": jornadas_importadas,
        "mapas": mapas_importados,
        "ignoradas": jornadas_ignoradas
    }