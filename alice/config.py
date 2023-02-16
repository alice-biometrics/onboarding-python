from typing import Union

from pydantic.fields import Field
from pydantic.main import BaseModel
from pydantic.types import confloat
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
    timeout: Union[confloat(ge=1, le=100), None] = Field(
        default=None,
        description="Timeout for every request in seconds",
    )
    send_agent: bool = Field(default=True)
    verbose: bool = Field(default=False)
    session: Union[Session, None] = None
