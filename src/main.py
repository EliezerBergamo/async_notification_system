"""
Módulo principal da API FastAPI para o sistema de notificação assíncrona.

Este módulo define os endpoints HTTP para o envio e consulta de notificações.
Ele atua como o ponto de entrada da aplicação, gerenciando o ciclo de vida
da conexão com o RabbitMQ e roteando as requisições de notificação para
o pipeline de mensageria.
"""

import json
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from typing import Dict, Any
from .rabbitmq_service import ServiceRabbitMQ
from .models import NotificacaoPayload
from .persistence import notification_status_create, notification_status_get

service_rabbitmq = ServiceRabbitMQ()

db_em_memoria: Dict[uuid.UUID, Any] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerenciador do ciclo de vida da aplicação.

    Estabelece e encerra a conexão com o RabbitMQ quando a aplicação
    é iniciada e encerrada, garantindo que os recursos sejam
    gerenciados corretamente.
    """
    print("Aplicação iniciando...")
    await service_rabbitmq.connect()
    yield
    print("Aplicação encerrando...")
    await service_rabbitmq.close()

app = FastAPI(lifespan=lifespan)

@app.post("/api/notificar", status_code=202)
async def notificar(payload: NotificacaoPayload):
    """
    Endpoint para o envio de uma nova notificação.

    - **Recebe:** um payload JSON com 'mensagemId', 'conteudoMensagem' e 'tipoNotificacao'.
    - **Valida:** o payload automaticamente com o modelo Pydantic 'NotificacaoPayload'.
    - **Gera:** um 'traceId' único para rastreamento.
    - **Persiste:** o status inicial ('RECEBIDO') da notificação em memória.
    - **Publica:** a mensagem em formato JSON na fila de entrada do RabbitMQ.
    - **Retorna:** um status 202 (Accepted) com 'traceId' e 'mensagemId', indicando
      que o processamento será realizado de forma assíncrona.
    """
    trace_id = uuid.uuid4()

    notificacao_status = {
        "traceId": trace_id,
        "mensagemId": payload.mensagemId,
        "conteudoMensagem": payload.conteudoMensagem,
        "tipoNotificacao": payload.tipoNotificacao,
        "status": "RECEBIDO"
    }

    notification_status_create(notificacao_status)

    rabbitmq_payload = {
        "traceId": str(trace_id),
        "mensagemId": str(payload.mensagemId),
        "conteudoMensagem": payload.conteudoMensagem,
        "tipoNotificacao": payload.tipoNotificacao,
    }

    fila_entrada = "fila.notificacao.entrada.ELIEZER"
    await service_rabbitmq.publish_message(fila_entrada, json.dumps(rabbitmq_payload))

    return {
        "mensagemId": payload.mensagemId,
        "traceId": trace_id,
        "status": "Requisição recebida e executada de forma assíncrona."
    }

@app.get("/api/notificacao/status/{traceId}")
async def get_notificacao_status(traceId: uuid.UUID):
    """
    Endpoint para consultar o status de uma notificação.

    - **Recebe:** um 'traceId' na URL.
    - **Busca:** o status mais recente da notificação na estrutura de dados em memória.
    - **Retorna:** os dados completos da notificação se encontrados.
    - **Levanta:** uma exceção HTTP 404 (Not Found) se o 'traceId' não existir.
    """
    status_data = notification_status_get(traceId)
    if not status_data:
        raise HTTPException(status_code=404, detail="Notificação não encontrada.")
    return status_data
