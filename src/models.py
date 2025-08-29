"""
Módulo de modelos de dados para a API de notificação.

Define os modelos Pydantic (BaseModel) para validação e serialização
dos dados, garantindo que o formato das requisições e a estrutura
do estado da notificação estejam corretos.
"""

import uuid
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class NotificacaoPayload(BaseModel):
    """
    Modelo para a validação do payload da requisição de notificação.

    Define a estrutura e as regras de validação para os dados de entrada
    recebidos pelo endpoint POST /api/notificar.

    Atributos:
        mensagemId (Optional[uuid.UUID]): Identificador único da mensagem.
            Gerado automaticamente se não for fornecido.
        conteudoMensagem (str): O conteúdo textual da notificação.
        tipoNotificacao (str): O tipo da notificação (e.g., "EMAIL", "SMS", "PUSH").
            A validação garante que o valor seja um dos tipos permitidos.
    """
    mensagemId: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)
    conteudoMensagem: str
    tipoNotificacao: str

    @field_validator('tipoNotificacao')
    def validar_tipo_notificacao(cls, v):
        """
            Valida que o 'tipoNotificacao' seja um dos valores permitidos.
            """
        allowed_types = {"EMAIL", "SMS", "PUSH"}
        if v.upper() not in allowed_types:
            raise ValueError(f"Tipo inválido."
                             f"Use um desses: {', '.join(allowed_types)}")
        return v.upper()

class NotificacaoStatus(BaseModel):
    """
    Modelo para o status da notificação armazenado em memória.

    Define a estrutura dos dados que representam o estado atual de uma
    notificação no sistema, utilizado para consulta pelo endpoint GET.

    Atributos:
        traceId (uuid.UUID): Identificador único de rastreamento para toda a vida da notificação.
        mensagemId (uuid.UUID): Identificador original da mensagem.
        conteudoMensagem (str): O conteúdo da notificação.
        tipoNotificacao (str): O tipo da notificação.
        status (str): O status atual da notificação no pipeline.
    """
    traceId: uuid.UUID
    mensagemId: uuid.UUID
    conteudoMensagem: str
    tipoNotificacao: str
    status: str