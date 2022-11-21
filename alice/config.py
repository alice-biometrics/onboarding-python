from typing import Union

from pydantic.dataclasses import dataclass


@dataclass
class Config:
    onboarding_url: str = "https://apis.alicebiometrics.com/onboarding"
    sandbox_url: str = "https://apis.alicebiometrics.com/onboarding/sandbox"
    api_key: Union[str, None] = None
    sandbox_token: Union[str, None] = None
    send_agent: bool = True
    verbose: bool = False
