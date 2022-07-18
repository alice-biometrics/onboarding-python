from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel


class DeviceOut(BaseModel):
    """
    It collects info about a device
    """

    agent: str = Field(description="Alice SDK")
    agent_version: str = Field(description="Alice SDK version")
    platform: str
    platform_version: str
    model: str
    ip: Optional[str] = None

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    @staticmethod
    def from_event(event):
        if not event.event_meta:
            return None

        device = event.event_meta.get("device")
        if not device:
            return None
        ip = event.event_info_id.get("ip") if event.event_info_id else None

        return DeviceOut(
            agent=device.get("agent"),
            agent_version=device.get("agent_version"),
            platform=device.get("platform"),
            platform_version=device.get("platform_version"),
            model=device.get("model"),
            ip=ip,
        )
