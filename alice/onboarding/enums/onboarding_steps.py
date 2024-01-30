from enum import Enum
from typing import Union

from pydantic import BaseModel


class OnboardingStepName(Enum):
    SELFIE = "selfie"
    SELFIE_WITH_CHALLENGE = "selfie_with_challenge"
    IDCARD = "idcard"
    DRIVER_LICENSE = "driverlicense"
    RESIDENCE_PERMIT = "residencepermit"
    HEALTH_INSURANCE_CARD = "healthinsurancecard"
    PASSPORT = "passport"
    OTHER_TRUSTED_DOCUMENT = "otd"
    ANY_DOCUMENT = "anydocument"


class OnboardingStepConfig(BaseModel):
    title: str
    category: str


class OnboardingStep(BaseModel):
    step: OnboardingStepName
    config: Union[OnboardingStepConfig, None] = None
