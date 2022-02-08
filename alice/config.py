from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class Config:
    onboarding_url: str = "https://apis.alicebiometrics.com/onboarding"
    sandbox_url: str = "https://apis.alicebiometrics.com/onboarding/sandbox"
    api_key: str = None
    sandbox_token: str = None
    send_agent: Optional[bool] = True
    verbose: Optional[bool] = False
