from typing import Optional

from pydantic import BaseModel


class DeviceInfo(BaseModel):
    device_platform: Optional[str] = None
    device_platform_version: Optional[str] = None
    device_model: Optional[str] = None
