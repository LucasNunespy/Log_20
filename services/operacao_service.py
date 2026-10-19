# services/operacao_service.py
from models.mapas import Mapa
from models.entregas import Entrega
from sqlalchemy import func

def consultar_total_mapas(data_inicio=None, data_fim=None):
    consulta = Mapa.query

    if data_inicio is not None:
        consulta = consulta.filter(
            Mapa.data_operacao >= data_inicio
        )

    if data_fim is not None:
        consulta = consulta.filter(
            Mapa.data_operacao <= data_fim
        )

    total = consulta.count()

    return total


    

def consultar_total_clientes(data_inicio=None, data_fim=None):
    consulta = Entrega.query.join(
        Mapa, Entrega.mapa_id == Mapa.id
    )

    if data_inicio is not None:
        consulta = consulta.filter(
            Mapa.data_operacao >= data_inicio
        )

    if data_fim is not None:
        consulta = consulta.filter(
            Mapa.data_operacao <= data_fim
        )

    total = consulta.count()

    return total



def consultar_total_devolucoes(data_inicio=None, data_fim=None):
    consulta = Entrega.query.join(
        Mapa, Entrega.mapa_id == Mapa.id
    )

    consulta = consulta.filter(
        Entrega.status.in_([
            "DEFINITELY_RETURNED",
            "PARTIAL_DELIVERY"
        ])
    )

    if data_inicio is not None:
        consulta = consulta.filter(
            Mapa.data_operacao >= data_inicio
        )

    if data_fim is not None:
        consulta = consulta.filter(
            Mapa.data_operacao <= data_fim
        )

    total = consulta.count()

    return total



def calcular_percentual_devolucao(data_inicio=None, data_fim=None):
    clientes = consultar_total_clientes(data_inicio, data_fim)
    devolucoes = consultar_total_devolucoes(data_inicio, data_fim)

    if clientes == 0:
        return 0

    percentual = (devolucoes / clientes) * 100

    return round(percentual, 2)




def consultar_motivos_devolucao(data_inicio=None, data_fim=None):
    consulta = Entrega.query.join(
        Mapa, Entrega.mapa_id == Mapa.id
    )

    consulta = consulta.with_entities(
        Entrega.motivo_devolucao,
        func.count(Entrega.id)
    )

    consulta = consulta.filter(
        Entrega.status.in_([
            "DEFINITELY_RETURNED",
            "PARTIAL_DELIVERY"
        ])
    )

    if data_inicio is not None:
        consulta = consulta.filter(
            Mapa.data_operacao >= data_inicio
        )

    if data_fim is not None:
        consulta = consulta.filter(
            Mapa.data_operacao <= data_fim
        )

    resultados = consulta.group_by(
        Entrega.motivo_devolucao
    ).all()

    motivos = []

    for motivo, quantidade in resultados:
        motivos.append({
            "motivo": motivo,
            "quantidade": quantidade
        })

    return motivos

def consultar_resumo_operacao(data_inicio=None, data_fim=None):
    resumo = {
        "total_mapas": consultar_total_mapas(data_inicio, data_fim),
        "total_clientes": consultar_total_clientes(data_inicio, data_fim),
        "total_devolucoes": consultar_total_devolucoes(data_inicio, data_fim),
        "percentual_devolucao": calcular_percentual_devolucao(data_inicio, data_fim),
        "motivos_devolucao": consultar_motivos_devolucao(data_inicio, data_fim)
    }

    return resumo