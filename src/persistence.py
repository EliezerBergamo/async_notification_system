"""
Módulo de persistência de dados em memória.

Este módulo gerencia o estado das notificações usando uma estrutura de dados
em memória (um dicionário Python). As funções aqui permitem a criação,
atualização e consulta do status das notificações com base em seu traceId,
simulando um armazenamento de dados para fins de rastreamento.
"""

from typing import Dict, Any
from uuid import UUID

db_em_memoria: Dict[UUID, Any] = {}

def notification_status_create(data: dict):
    """
    Cria e armazena o status inicial de uma notificação.

    Args:
        data (dict): Dicionário contendo os dados da notificação,
                     incluindo o traceId.
    """
    trace_id = data.get("traceId")
    if trace_id:
        db_em_memoria[trace_id] = data
        print(f"Status inicial da notificação {trace_id} criado: RECEBIDO")

def notification_status_update(trace_id: UUID, new_status: str):
    """
    Atualiza o status de uma notificação existente.

    Args:
        trace_id (UUID): O UUID da notificação a ser atualizada.
        new_status (str): O novo status a ser atribuído (e.g., "PROCESSADO_INTERMEDIARIO").
    """
    if trace_id in db_em_memoria:
        db_em_memoria[trace_id]['status'] = new_status
        print(f"Status da notificação {trace_id} atualizado para: {new_status}")

def notification_status_get(trace_id: UUID):
    """
    Retorna os dados completos do status de uma notificação.

    Args:
        trace_id (UUID): O UUID da notificação a ser consultada.

    Returns:
        Dict[str, Any] | None: O dicionário com os dados da notificação ou
                              None se o traceId não for encontrado.
    """
    return db_em_memoria.get(trace_id)