from enum import Enum
from typing import Any, Dict, Union

from pydantic import BaseModel


class OnboardingStepName(str, Enum):
    SELFIE = "selfie"
    SELFIE_WITH_CHALLENGE = "selfie_with_challenge"
    IDCARD = "idcard"
    DRIVER_LICENSE = "driverlicense"
    RESIDENCE_PERMIT = "residencepermit"
    HEALTH_INSURANCE_CARD = "healthinsurancecard"
    PASSPORT = "passport"
    OTHER_TRUSTED_DOCUMENT = "otd"
    ANY_DOCUMENT = "anydocument"


class OnboardingStep(BaseModel):
    name: OnboardingStepName
    config: Union[Dict[str, Any], None] = None
