"""
Módulo de serviço para gerenciamento da conexão e publicação de mensagens no RabbitMQ.

Este módulo encapsula toda a lógica de interação com o RabbitMQ, garantindo
que a conexão e o canal sejam gerenciados de forma centralizada e robusta.
Ele fornece métodos para conectar, desconectar e publicar mensagens, isolando
a lógica de mensageria do restante da aplicação.
"""

import os
import aio_pika
from dotenv import load_dotenv

load_dotenv()

class ServiceRabbitMQ:
    """
    Gerencia a conexão e o canal do RabbitMQ para a aplicação.

    A conexão é feita usando a URL fornecida na variável de ambiente
    RABBITMQ_URL. O método `connect` é assíncrono e deve ser chamado
    para estabelecer a conexão.
    """
    def __init__(self):
        """
        Inicializa o serviço, carregando a URL de conexão do ambiente.

        Raises:
            ValueError: Se a variável de ambiente RABBITMQ_URL não estiver definida.
        """
        self.connection = None
        self.channel = None
        self.url = os.getenv("RABBITMQ_URL")
        if not self.url:
            raise ValueError("Variável de ambiente RABBITMQ_URL não foi definida."
                             "Verificar o arquivo .env")

    async def connect(self):
        """
        Estabelece uma conexão robusta e um canal com o RabbitMQ.

        Utiliza `aio_pika.connect_robust` para garantir reconexão automática
        em caso de falha. A conexão e o canal são armazenados como atributos
        da classe para reutilização.

        Raises:
        ConnectionError: Se não for possível estabelecer a conexão após
                         as tentativas de reconexão.
        """
        try:
            self.connection = await aio_pika.connect_robust(self.url)
            self.channel = await self.connection.channel()
            print("Conexão do RabbitMQ estabelecida.")
        except Exception as e:
            print(f"Erro de conexão com o RabbitMQ: {e}")
            # Levanta a exceção para que o código saiba que a conexão falhou
            raise ConnectionError("Não foi possível conectar ao RabbitMQ.") from e

    async def close(self):
        """
        Encerra a conexão ativa com o RabbitMQ.

        Verifica se a conexão existe e não está fechada antes de tentar
        encerrá-la, evitando erros.
        """
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            print("Conexão do RabbitMQ encerrada.")

    async def publish_message(self, queue_name: str, message_body: str):
        """
        Publica uma mensagem em uma fila específica do RabbitMQ.

        Verifica se o canal está disponível e tenta reconectar
        automaticamente caso contrário, demonstrando resiliência.

        Args:
            queue_name (str): O nome da fila para onde a mensagem será enviada.
            message_body (str): O conteúdo da mensagem a ser publicada.
        """
        if not self.channel:
            print("Canal do RabbitMQ indisponível. Tentando reconectar...")
            # Tentar reconectar, se o canal estiver indisponível
            await self.connect()
            if not self.channel:
                print("Reconexão falhou. Não foi possível publicar a mensagem.")
                return

        try:
            await self.channel.default_exchange.publish(
                aio_pika.Message(body=message_body.encode()),
                routing_key=queue_name,
            )
            print(f"Mensagem publicada: {queue_name}")
        except Exception as e:
            print(f"Falha ao publicar mensagem: {e}")