"""
Data model module for the notification API.

Defines the Pydantic models (BaseModel) for validation and serialization
of data, ensuring that the format of requests and the structure
of the notification status are correct.
"""

import uuid
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class NotificationPayload(BaseModel):
    """
    Template for validating the notification request payload.

    Defines the structure and validation rules for input data
    received by the POST /api/notify endpoint.

    Attributes:
        messageId (Optional[uuid.UUID]): Unique message identifier.
            Automatically generated if not provided.
        contentMessage (str): The textual content of the notification.
        typeNotification (str): The type of notification (e.g., “EMAIL,” “SMS,” “PUSH”).
            Validation ensures that the value is one of the allowed types.

    """
    messageId: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)
    contentMessage: str
    typeNotification: str

    @field_validator('typeNotification')
    def validate_notification_type(cls, v):
        """
        Validates that ‘typeNotification’ is one of the allowed values.
        """
        allowed_types = {"EMAIL", "SMS", "PUSH"}
        if v.upper() not in allowed_types:
            raise ValueError(f"Invalid type."
                             f"Use one of these: {', '.join(allowed_types)}")
        return v.upper()

class NotificationStatus(BaseModel):
    """
    Template for the notification status stored in memory.

    Defines the structure of the data representing the current status of a
    notification in the system, used for querying by the GET endpoint.

    Attributes:
        traceId (uuid.UUID): Unique tracking identifier for the entire life of the notification.
        messageId (uuid.UUID): Original message identifier.
        contentMessage (str): The content of the notification.
        typeNotification (str): The type of notification.
        status (str): The current status of the notification in the pipeline.
    """
    traceId: uuid.UUID
    messageId: uuid.UUID
    contentMessage: str
    typeNotification: str
    status: str