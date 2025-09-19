"""
Service module for managing connections and publishing messages in RabbitMQ.

This module encapsulates all logic for interacting with RabbitMQ, ensuring
that connections and channels are managed in a centralized and robust manner.
It provides methods for connecting, disconnecting, and publishing messages, isolating
the messaging logic from the rest of the application.
"""

import os
import aio_pika
from dotenv import load_dotenv

load_dotenv()

class ServiceRabbitMQ:
    """
    Manages the RabbitMQ connection and channel for the application.

    The connection is made using the URL provided in the
    RABBITMQ_URL environment variable. The `connect` method is asynchronous and must be called
    to establish the connection.
    """
    def __init__(self):
        """
         Initializes the service by loading the environment connection URL.

        Raises:
            ValueError: If the RABBITMQ_URL environment variable is not defined.
        """
        self.connection = None
        self.channel = None
        self.url = os.getenv("RABBITMQ_URL")
        if not self.url:
            raise ValueError("Environment variable RABBITMQ_URL has not been defined."
                             "Check the .env file")

    async def connect(self):
        """
        Establishes a robust connection and channel with RabbitMQ.

        Uses `aio_pika.connect_robust` to ensure automatic reconnection
        in case of failure. The connection and channel are stored as attributes
        of the class for reuse.

        Raises:
            ConnectionError: If the connection cannot be established after reconnection attempts.
        """
        try:
            self.connection = await aio_pika.connect_robust(self.url)
            self.channel = await self.connection.channel()
            print("RabbitMQ connection established.")
        except Exception as e:
            print(f"Connection error with RabbitMQ: {e}")
            raise ConnectionError("Unable to connect to RabbitMQ.") from e

    async def close(self):
        """
        Closes the active connection to RabbitMQ.

        Checks if the connection exists and is not closed before attempting to close it, avoiding errors.
        """
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            print("RabbitMQ connection closed.")

    async def publish_message(self, queue_name: str, message_body: str):
        """
        Publishes a message to a specific RabbitMQ queue.

        Checks if the channel is available and automatically attempts to reconnect
        if not, demonstrating resilience.

        Args:
            queue_name (str): The name of the queue to which the message will be sent.
            message_body (str): The content of the message to be published.
        """
        if not self.channel:
            print("RabbitMQ channel unavailable. Attempting to reconnect...")
            await self.connect()
            if not self.channel:
                print("Reconnection failed. The message could not be posted.")
                return

        try:
            await self.channel.default_exchange.publish(
                aio_pika.Message(body=message_body.encode()),
                routing_key=queue_name,
            )
            print(f"Message posted: {queue_name}")
        except Exception as e:
            print(f"Failed to post message: {e}")