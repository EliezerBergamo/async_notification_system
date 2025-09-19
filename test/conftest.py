"""
Shared fixtures module for pytest tests.

This file is automatically read by pytest, and the fixtures defined here
can be used in any test in the same folder or subfolders.
It centralizes the configuration of mock objects to ensure
consistency and reuse in tests.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def service_rabbitmq_mock():
    """
    Creates and returns a mock for the ServiceRabbitMQ class.

    This fixture simulates the behavior of the actual `ServiceRabbitMQ` class without
    establishing a network connection. This allows you to test the application logic
    in isolation and quickly.

    The `connect`, `close`, and `publish_message` methods are replaced by
    `AsyncMock`, which allows you to verify that they were called and with which arguments.

    Returns:
        MagicMock: A mock object that simulates the ServiceRabbitMQ class.
    """

    mock_service = MagicMock()
    mock_service.connect = AsyncMock()
    mock_service.close = AsyncMock()

    mock_service.publish_message = AsyncMock()

    return mock_service