from enum import Enum


class OnboardingSteps(Enum):
    SELFIE = "selfie"
    SELFIE_WITH_CHALLENGE = "selfie_with_challenge"
    IDCARD = "idcard"
    DRIVER_LICENSE = "driverlicense"
    RESIDENCE_PERMIT = "residencepermit"
    HEALTH_INSURANCE_CARD = "healthinsurancecard"
    PASSPORT = "passport"
    OTHER_TRUSTED_DOCUMENT = "otd"
    ANY_DOCUMENT = "anydocument"
