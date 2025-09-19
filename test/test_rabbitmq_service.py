"""
Unit testing module for the notification API.

This file contains tests to ensure that the notification endpoint
behaves as expected, focusing on its interaction with the external service
(RabbitMQ) in isolation, without the need for an
actual network connection.

The fixtures in the `conftest.py` module are used to simulate the
behavior of the RabbitMQ service, ensuring that the business logic
is tested efficiently and reliably.

Translated with DeepL.com (free version)
"""

import pytest
import json
from fastapi.testclient import TestClient
from src.main import app, service_rabbitmq
from .conftest import service_rabbitmq_mock

API_URL = "/api/notify"


@pytest.mark.asyncio
async def test_publish_message_is_called_with_correct_arguments(service_rabbitmq_mock):
    """
    Tests whether the RabbitMQ service's `publish_message` method is called
    with the correct arguments.

    The `service_rabbitmq_mock` fixture is injected to simulate the
    actual service. The test logic is as follows:
    1. Replaces the actual service instance with the mock.
    2. Sends a POST request to the API endpoint.
    3. Checks that the response status is 202 (Accepted).
    4. Asserts that `publish_message` was called exactly once.
    5. Extracts the arguments from the call and validates them.
    6. Validates the queue name and the content of the published message.
    """
    service_rabbitmq.publish_message = service_rabbitmq_mock.publish_message

    test_payload = {
        "contentMessage": "Hello, this is a test message.",
        "typeNotification": "EMAIL"
    }

    client = TestClient(app)

    response = client.post(API_URL, json=test_payload)

    assert response.status_code == 202

    service_rabbitmq_mock.publish_message.assert_awaited_once()

    call_args = service_rabbitmq_mock.publish_message.await_args.args

    published_message_data = json.loads(call_args[1])

    assert call_args[0] == "fila.notification.entry.NAME"
    assert published_message_data['contentMessage'] == "Hello, this is a test message."
    assert published_message_data['typeNotification'] == "EMAIL"

    assert 'traceId' in published_message_data
    assert 'messageId' in published_message_data