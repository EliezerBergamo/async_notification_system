"""
Módulo de fixtures compartilhadas para os testes do pytest.

Este arquivo é lido automaticamente pelo pytest e as fixtures definidas aqui
podem ser usadas em qualquer teste na mesma pasta ou subpastas.
Ele centraliza a configuração de objetos simulados (mocks) para garantir
consistência e reutilização nos testes.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def service_rabbitmq_mock():
    """
    Cria e retorna um mock para a classe ServiceRabbitMQ.

    Esta fixture simula o comportamento da classe real `ServiceRabbitMQ` sem
    estabelecer uma conexão de rede. Isso permite testar a lógica da aplicação
    de forma isolada e rápida.

    Os métodos `connect`, `close` e `publish_message` são substituídos por
    `AsyncMock`, que permite verificar se foram chamados e com quais argumentos.

    Returns:
        MagicMock: Um objeto mock que simula a classe ServiceRabbitMQ.
    """

    mock_service = MagicMock()
    mock_service.connect = AsyncMock()
    mock_service.close = AsyncMock()

    mock_service.publish_message = AsyncMock()

    return mock_service