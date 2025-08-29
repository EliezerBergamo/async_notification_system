"""
Módulo de consumidores para o sistema de notificação assíncrona.

Este script é responsável por iniciar e gerenciar todos os consumidores do
pipeline de mensagens do RabbitMQ. Ele estabelece uma conexão, declara
as filas e inicia o consumo de mensagens de forma assíncrona, de acordo
com as diferentes etapas do fluxo de trabalho.
"""

import asyncio
import os
import aio_pika
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL")

FILAS = {
    "entrada": "entrada",
    "validacao": "validacao",
    "retry": "retry",
    "dlq": "dlq",
}

async def entrada_process_message(message: aio_pika.IncomingMessage):
    """
    Callback para o consumidor da fila de entrada.

    Processa mensagens recebidas da fila de entrada, simulando
    a primeira etapa de processamento.
    """
    async with message.process():
        print(f"[entrada] Recebido: {message.body.decode()}")

async def validacao_process_message(message: aio_pika.IncomingMessage):
    """
    Callback para o consumidor da fila de validação.

    Processa mensagens que passaram pela etapa inicial e aguardam
    validação ou envio final.
    """
    async with message.process():
        print(f"[validacao] Recebido: {message.body.decode()}")

async def retry_process_message(message: aio_pika.IncomingMessage):
    """
    Callback para o consumidor da fila de reprocessamento.

    Recebe mensagens que falharam na etapa inicial e tenta reprocessá-las.
    """
    async with message.process():
        print(f"[retry] Recebido: {message.body.decode()}")

async def dlq_process_message(message: aio_pika.IncomingMessage):
    """
    Callback para o consumidor da Dead Letter Queue (DLQ).

    Recebe mensagens que falharam após todas as tentativas de
    reprocessamento e as marca como finalizadas (sem processamento posterior).
    """
    async with message.process():
        print(f"[dlq] Recebido: {message.body.decode()}")

async def start_consumers():
    """
    Função principal que inicia e gerencia o ciclo de vida dos consumidores.

    - Estabelece uma conexão robusta com o RabbitMQ.
    - Declara todas as filas necessárias para o pipeline.
    - Inicia o consumo assíncrono de mensagens em todas as filas.
    - Mantém a aplicação rodando indefinidamente.
    """
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    print("Conexão do RabbitMQ estabelecida.")

    async with connection:
        channel = await connection.channel()

        queue_entrada = await channel.declare_queue(FILAS["entrada"], durable=True)
        queue_validacao = await channel.declare_queue(FILAS["validacao"], durable=True)
        queue_retry = await channel.declare_queue(FILAS["retry"], durable=True)
        queue_dlq = await channel.declare_queue(FILAS["dlq"], durable=True)

        print("Filas do RabbitMQ declaradas. Iniciando consumidores...")

        await asyncio.gather(
            queue_entrada.consume(entrada_process_message),
            queue_validacao.consume(validacao_process_message),
            queue_retry.consume(retry_process_message),
            queue_dlq.consume(dlq_process_message),
        )

        print("Consumidores em execução. Aguardando mensagens...")

        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(start_consumers())
    except KeyboardInterrupt:
        print("Encerrando consumidores...")
