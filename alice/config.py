from typing import Union

from pydantic import BaseModel, Field
from requests import Session

from alice.onboarding.enums.environment import Environment


class Config(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    environment: Environment = Field(default=Environment.SANDBOX)
    api_key: Union[str, None] = Field(default=None)
    trial_token: Union[str, None] = Field(default=None)
    timeout: Union[float, None] = Field(
        default=None, description="Timeout for every request in seconds", ge=0, le=100
    )
    send_agent: bool = Field(default=True)
    verbose: bool = Field(default=False)
    session: Union[Session, None] = Field(default=None)
