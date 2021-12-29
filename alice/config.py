from pydantic import BaseModel


class Config(BaseModel):
    onboarding_url: str = "https://apis.alicebiometrics.com/onboarding"
    sandbox_url: str = "https://apis.alicebiometrics.com/onboarding/sandbox"
    api_key: str = None
    sandbox_token: str = None
    send_agent: bool = True
    verbose: bool = False
