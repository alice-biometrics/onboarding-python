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
    send_agent: bool = Field(default=True)
    verbose: bool = Field(default=False)
    session: Union[Session, None] = None
