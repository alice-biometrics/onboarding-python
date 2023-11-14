from typing import List

from pydantic import BaseModel

from alice.onboarding.models.report.compliance.device_out import DeviceOut
from alice.onboarding.models.report.compliance.domain_event import DomainEvent


class DomainEventsReport(BaseModel):
    devices: List[DeviceOut]
    events: List[DomainEvent]
    # num_devices: int
    # total_time: float  # seconds
