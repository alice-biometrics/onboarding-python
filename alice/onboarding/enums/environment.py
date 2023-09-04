from enum import Enum


class Environment(Enum):
    SANDBOX = "sandbox"
    PRODUCTION = "production"
    STAGING = "staging"

    def get_url(self) -> str:
        if self is Environment.SANDBOX:
            return "https://apis.sandbox.alicebiometrics.com/onboarding"
        elif self is Environment.PRODUCTION:
            return "https://apis.alicebiometrics.com/onboarding"
        else:
            return "https://apis.staging.alicebiometrics.com/onboarding"
