from typing import Union

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings
from requests import Session

from alice.onboarding.enums.environment import Environment


class Config(BaseSettings):
    class Config:
        arbitrary_types_allowed = True

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
    def validate_urls(cls, model: "Config") -> "Config":
        if model.environment is None:
            if "sandbox" in model.onboarding_url:
                model.environment = Environment.SANDBOX
            elif "staging" in model.onboarding_url:
                model.environment = Environment.STAGING
        else:
            if model.environment == Environment.PRODUCTION:
                model.onboarding_url = "https://apis.alicebiometrics.com/onboarding"
                model.sandbox_url = (
                    "https://apis.alicebiometrics.com/onboarding/sandbox"
                )
            elif model.environment == Environment.SANDBOX:
                model.onboarding_url = (
                    "https://apis.sandbox.alicebiometrics.com/onboarding"
                )
                model.sandbox_url = (
                    "https://apis.sandbox.alicebiometrics.com/onboarding/sandbox"
                )
            elif model.environment == Environment.STAGING:
                model.onboarding_url = (
                    "https://apis.staging.alicebiometrics.com/onboarding"
                )
                model.sandbox_url = (
                    "https://apis.staging.alicebiometrics.com/onboarding/sandbox"
                )
        return model
