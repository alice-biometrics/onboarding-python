from dataclasses import dataclass


@dataclass
class Config:
    onboarding_url: str = "https://pre.alicebiometrics.com/onboarding"
    sandbox_url: str = "https://pre.alicebiometrics.com/onboarding/sandbox"
    auth_url: str = "https://pre.alicebiometrics.com/auth"
    api_key: str = None
    sandbox_token: str = None
    send_agent: bool = True
