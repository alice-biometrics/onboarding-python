from typing import Union

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from requests import Session

from alice.onboarding.enums.environment import Environment


class Config(BaseSettings):
    model_config = SettingsConfigDict(arbitrary_types_allowed=True)

    api_key: Union[str, None] = Field(default=None)
    environment: Union[Environment, None] = Field(
        default=Environment.PRODUCTION, alias="ALICE_ENVIRONMENT"
    )
    verbose: bool = Field(default=False)
    session: Union[Session, None] = Field(default=None)
    timeout: Union[float, None] = Field(
        default=None, description="Timeout for every request in seconds", ge=0, le=100
    )
    send_agent: bool = Field(default=True)
    onboarding_url: Union[str, None] = Field(
        default="https://apis.alicebiometrics.com/onboarding"
    )
    sandbox_url: Union[str, None] = Field(
        default="https://apis.alicebiometrics.com/onboarding/sandbox",
        description="This path is only used for trials",
    )
    sandbox_token: Union[str, None] = Field(
        default=None, description="This token is only used for trials"
    )

    @model_validator(mode="after")
    def validate_urls(self) -> "Config":
        if self.environment is None or self.environment == Environment.PRODUCTION:
            if isinstance(self.onboarding_url, str):
                if "sandbox" in self.onboarding_url:
                    self.environment = Environment.SANDBOX
                elif "staging" in self.onboarding_url:
                    self.environment = Environment.STAGING
        else:
            if self.environment == Environment.SANDBOX:
                self.onboarding_url = (
                    "https://apis.sandbox.alicebiometrics.com/onboarding"
                )
                self.sandbox_url = (
                    "https://apis.sandbox.alicebiometrics.com/onboarding/sandbox"
                )
            elif self.environment == Environment.STAGING:
                self.onboarding_url = (
                    "https://apis.staging.alicebiometrics.com/onboarding"
                )
                self.sandbox_url = (
                    "https://apis.staging.alicebiometrics.com/onboarding/sandbox"
                )
        return self
