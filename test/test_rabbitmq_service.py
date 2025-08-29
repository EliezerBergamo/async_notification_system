"""
Módulo de testes unitários para a API de notificação.

Este arquivo contém testes para garantir que o endpoint de notificação
se comporte como esperado, focando em sua interação com o serviço
externo (RabbitMQ) de forma isolada, sem a necessidade de uma
conexão de rede real.

As fixtures do módulo `conftest.py` são usadas para simular o
comportamento do serviço RabbitMQ, garantindo que a lógica de
negócio seja testada de forma eficiente e confiável.
"""

import pytest
import json
from fastapi.testclient import TestClient
from src.main import app, service_rabbitmq
from .conftest import service_rabbitmq_mock

API_URL = "/api/notificar"


@pytest.mark.asyncio
async def test_publish_message_is_called_with_correct_arguments(service_rabbitmq_mock):
    """
    Testa se o método `publish_message` do serviço RabbitMQ é chamado
    com os argumentos corretos.

    A `fixture` `service_rabbitmq_mock` é injetada para simular o
    serviço real. A lógica do teste é a seguinte:
    1. Substitui a instância real do serviço pela mock.
    2. Envia uma requisição POST para o endpoint da API.
    3. Verifica se o status de resposta é 202 (Accepted).
    4. Afirma que `publish_message` foi chamado exatamente uma vez.
    5. Extrai os argumentos da chamada e os valida.
    6. Valida o nome da fila e o conteúdo da mensagem publicada.
    """
    service_rabbitmq.publish_message = service_rabbitmq_mock.publish_message

    test_payload = {
        "conteudoMensagem": "Olá, esta é uma mensagem de teste.",
        "tipoNotificacao": "EMAIL"
    }

    client = TestClient(app)

    response = client.post(API_URL, json=test_payload)

    assert response.status_code == 202

    service_rabbitmq_mock.publish_message.assert_awaited_once()

    call_args = service_rabbitmq_mock.publish_message.await_args.args

    published_message_data = json.loads(call_args[1])

    assert call_args[0] == "fila.notificacao.entrada.ELIEZER"
    assert published_message_data['conteudoMensagem'] == "Olá, esta é uma mensagem de teste."
    assert published_message_data['tipoNotificacao'] == "EMAIL"

    assert 'traceId' in published_message_data
    assert 'mensagemId' in published_message_data