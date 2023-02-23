from typing import Union

from pydantic.fields import Field
from pydantic.main import BaseModel
from requests import Session


class Config(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    onboarding_url: str = Field(default="https://apis.alicebiometrics.com/onboarding")
    sandbox_url: str = Field(
        default="https://apis.alicebiometrics.com/onboarding/sandbox"
    )
    api_key: Union[str, None] = Field(default=None)
    sandbox_token: Union[str, None] = Field(default=None)
    timeout: Union[float, None] = Field(
        default=None, description="Timeout for every request in seconds", ge=0, le=100
    )
    send_agent: bool = Field(default=True)
    verbose: bool = Field(default=False)
    session: Union[Session, None] = None
