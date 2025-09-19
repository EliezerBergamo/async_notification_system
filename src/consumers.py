"""
Consumer module for the asynchronous notification system.

This script is responsible for starting and managing all consumers in the
RabbitMQ message pipeline. It establishes a connection, declares the
QUEUES, and starts consuming messages asynchronously, according to the
different stages of the workflow.
"""

import asyncio
import os
import aio_pika
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL")

QUEUES = {
    "entry": "entry",
    "validation": "validation",
    "retry": "retry",
    "dlq": "dlq",
}

async def entry_process_message(message: aio_pika.IncomingMessage):
    """
    Callback to the consumer of the entry queue.

    Processes messages received from the entry queue, simulating
    the first stage of processing.
    """
    async with message.process():
        print(f"[entry] Received: {message.body.decode()}")

async def validation_process_message(message: aio_pika.IncomingMessage):
    """
    Callback to the consumer of the validation queue.

    Processes messages that have passed the initial stage and are awaiting
    validation or final delivery.
    """
    async with message.process():
        print(f"[validation] Received: {message.body.decode()}")

async def retry_process_message(message: aio_pika.IncomingMessage):
    """
    Callback for the reprocessing queue consumer.

    Receives messages that failed in the initial stage and attempts to reprocess them.
    """
    async with message.process():
        print(f"[retry] Received: {message.body.decode()}")

async def dlq_process_message(message: aio_pika.IncomingMessage):
    """
    Callback for the Dead Letter Queue (DLQ) consumer.

    Receives messages that failed after all reprocessing attempts
    and marks them as finished (no further processing).
    """
    async with message.process():
        print(f"[dlq] Received: {message.body.decode()}")

async def start_consumers():
    """
    Main function that starts and manages the consumer lifecycle.

    - Establishes a robust connection with RabbitMQ.
    - Declares all queues needed for the pipeline.
    - Starts asynchronous message consumption on all queues.
    - Keeps the application running indefinitely.
    """
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    print("RabbitMQ connection established.")

    async with connection:
        channel = await connection.channel()

        queue_entry = await channel.declare_queue(QUEUES["entry"], durable=True)
        queue_validation = await channel.declare_queue(QUEUES["validation"], durable=True)
        queue_retry = await channel.declare_queue(QUEUES["retry"], durable=True)
        queue_dlq = await channel.declare_queue(QUEUES["dlq"], durable=True)

        print("RabbitMQ queues declared. Starting consumers...")

        await asyncio.gather(
            queue_entry.consume(entry_process_message),
            queue_validation.consume(validation_process_message),
            queue_retry.consume(retry_process_message),
            queue_dlq.consume(dlq_process_message),
        )

        print("Consumers running. Waiting for messages...")

        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(start_consumers())
    except KeyboardInterrupt:
        print("Closing consumers...")
