from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from alice.onboarding.models.report.compliance.device_out import DeviceOut


class UserEventOut(BaseModel):
    """
    It collects events info
    """

    type: str = Field(description="Event type")
    id: UUID = Field(description="Unique event identifier (UUID v4 standard)")
    occurred_on: datetime = Field(description="Event time in ISO 8601 format")
    attributes: Optional[Dict[str, Any]] = Field(description="Event Attributes")
    device: Optional[DeviceOut] = Field(
        description="Device on which the event occurred"
    )
