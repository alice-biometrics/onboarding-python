from typing import Optional

from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class DeviceInfo:
    device_platform: Optional[str] = None
    device_platform_version: Optional[str] = None
    device_model: Optional[str] = None
