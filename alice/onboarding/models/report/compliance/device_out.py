from typing import Union

from pydantic import BaseModel, Field


class DeviceOut(BaseModel):
    """
    It collects info about a device
    """

    agent: str = Field(description="Alice SDK")
    agent_version: str = Field(description="Alice SDK version")
    platform: str
    platform_version: str
    model: str
    ip: Union[str, None] = Field(default=None)

    def __hash__(self) -> int:
        return hash((type(self),) + tuple(self.__dict__.values()))
