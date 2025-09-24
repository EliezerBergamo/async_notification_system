"""
Main module of the FastAPI API for the asynchronous notification system.

This module defines the HTTP endpoints for sending and querying notifications.
It acts as the application's entry point, managing the lifecycle
of the connection to RabbitMQ and routing notification requests to
the messaging pipeline.
"""

import json
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from typing import Dict, Any
from .rabbitmq_service import ServiceRabbitMQ
from .models import NotificationPayload
from .persistence import notification_status_create, notification_status_get

service_rabbitmq = ServiceRabbitMQ()

db_in_memory: Dict[uuid.UUID, Any] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle manager.

    Establishes and terminates the connection with RabbitMQ when the application
    is started and terminated, ensuring that resources are
    managed correctly.
    """
    print("Application starting...")
    await service_rabbitmq.connect()
    yield
    print("Application closing...")
    await service_rabbitmq.close()

app = FastAPI(lifespan=lifespan)

@app.post("/api/notify", status_code=202)
async def notify(payload: NotificationPayload):
    """
    Endpoint for sending a new notification.

    - Receives: a JSON payload with ‘messageId’, ‘contentMessage’, and ‘typeNotification’.
    - Validates: the payload automatically with the Pydantic ‘notificationPayload’ model.
    - Generates: a unique ‘traceId’ for tracking.
    - Persists: the initial status (‘RECEIVED’) of the notification in memory.
    - Publishes: the message in JSON format to the RabbitMQ entry queue.
    - Returns:** a 202 (Accepted) status with ‘traceId’ and ‘messageId’, indicating
      that processing will be performed asynchronously.
    """
    trace_id = uuid.uuid4()

    notification_status = {
        "traceId": trace_id,
        "messageId": payload.messageId,
        "contentMessage": payload.contentMessage,
        "typeNotification": payload.typeNotification,
        "status": "RECEIVED"
    }

    notification_status_create(notification_status)

    rabbitmq_payload = {
        "traceId": str(trace_id),
        "messageId": str(payload.messageId),
        "contentMessage": payload.contentMessage,
        "typeNotification": payload.typeNotification,
    }

    queue_entry = "queue.notification.entry.NAME"
    await service_rabbitmq.publish_message(queue_entry, json.dumps(rabbitmq_payload))

    return {
        "messageId": payload.messageId,
        "traceId": trace_id,
        "status": "Request received and executed asynchronously."
    }

@app.get("/api/notification/status/{traceId}")
async def get_notification_status(traceId: uuid.UUID):
    """
    Endpoint to query the status of a notification.

    - Receives: a ‘traceId’ in the URL.
    - Searches: the most recent status of the notification in the in-memory data structure.
    - Returns: the complete notification data if found.
    - Raises: an HTTP 404 (Not Found) exception if the ‘traceId’ does not exist.
    """
    status_data = notification_status_get(traceId)
    if not status_data:
        raise HTTPException(status_code=404, detail="Notification not found.")
    return status_data
