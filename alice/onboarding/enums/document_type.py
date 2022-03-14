from enum import Enum


class DocumentType(Enum):
    ID_CARD = "idcard"
    DRIVER_LICENSE = "driverlicense"
    RESIDENCE_PERMIT = "residencepermit"
    PASSPORT = "passport"
    HEALTH_INSURANCE_CARD = "healthinsurancecard"
