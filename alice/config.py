from typing import Optional

from pydantic.dataclasses import dataclass
from requests import Session


class PydanticConfig:
    arbitrary_types_allowed = True


@dataclass(config=PydanticConfig)
class Config:
    onboarding_url: str = "https://apis.alicebiometrics.com/onboarding"
    sandbox_url: str = "https://apis.alicebiometrics.com/onboarding/sandbox"
    api_key: str = None
    sandbox_token: str = None
    send_agent: Optional[bool] = True
    verbose: Optional[bool] = False
    session: Optional[Session] = None
