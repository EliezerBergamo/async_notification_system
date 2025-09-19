"""
In-memory data persistence module.

This module manages the status of notifications using an in-memory data structure
(a Python dictionary). The functions here allow the creation,
updating, and querying of notification status based on their traceId,
simulating data storage for tracking purposes.
"""

from typing import Dict, Any
from uuid import UUID

db_in_memory: Dict[UUID, Any] = {}

def notification_status_create(data: dict):
    """
    Creates and stores the initial status of a notification.

    Args:
        data (dict): Dictionary containing the notification data,
                     including the traceId.
    """
    trace_id = data.get("traceId")
    if trace_id:
        db_in_memory[trace_id] = data
        print(f"Initial notification status {trace_id} created: RECEIVED")

def notification_status_update(trace_id: UUID, new_status: str):
    """
    Updates the status of an existing notification.

    Args:
        trace_id (UUID): The UUID of the notification to be updated.
        new_status (str): The new status to be assigned (e.g., “PROCESSED_INTERMEDIATE”).
    """
    if trace_id in db_in_memory:
        db_in_memory[trace_id]['status'] = new_status
        print(f"Notification status {trace_id} updated to: {new_status}")

def notification_status_get(trace_id: UUID):
    """
    Returns the complete status data for a notification.

    Args:
        trace_id (UUID): The UUID of the notification to be queried.

    Returns:
        Dict[str, Any] | None: The dictionary with the notification data or
                              None if the traceId is not found.
    """
    return db_in_memory.get(trace_id)