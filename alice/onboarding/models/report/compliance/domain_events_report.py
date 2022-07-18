from typing import List

from pydantic.main import BaseModel

from alice.onboarding.models.report.compliance.device_out import DeviceOut
from alice.onboarding.models.report.compliance.user_event_out import UserEventOut


class DomainEventsReport(BaseModel):
    devices: List[DeviceOut]
    events: List[UserEventOut]
    # num_devices: int
    # total_time: float  # seconds
