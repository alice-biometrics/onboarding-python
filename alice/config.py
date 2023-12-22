from typing import Union

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from requests import Session

from alice.onboarding.enums.environment import Environment


class Config(BaseSettings):
    model_config = SettingsConfigDict(arbitrary_types_allowed=True, extra="allow")

    api_key: Union[str, None] = Field(default=None)
    environment: Union[Environment, None] = Field(
        default=Environment.PRODUCTION  # , validation_alias="ALICE_ENVIRONMENT"
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
    face_url: Union[str, None] = Field(default="https://apis.alicebiometrics.com/face")
    sandbox_url: Union[str, None] = Field(
        default="https://apis.alicebiometrics.com/onboarding/sandbox",
        description="This path is only used for trials",
    )
    sandbox_token: Union[str, None] = Field(
        default=None, description="This token is only used for trials"
    )
    use_cache: bool = Field(
        default=True,
        description="This optional feature allows users to configure specific caches during service invocation, optimizing the performance of the application.",
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
            self.onboarding_url = (
                f"https://apis.{self.environment.value}.alicebiometrics.com/onboarding"
            )
            self.face_url = (
                f"https://apis.{self.environment.value}.alicebiometrics.com/face"
            )
            self.sandbox_url = f"https://apis.{self.environment.value}.alicebiometrics.com/onboarding/sandbox"

        return self
