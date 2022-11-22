from enum import Enum


class DocumentType(Enum):
    ID_CARD = "idcard"
    DRIVER_LICENSE = "driverlicense"
    RESIDENCE_PERMIT = "residencepermit"
    PASSPORT = "passport"
    HEALTH_INSURANCE_CARD = "healthinsurancecard"


DOC_NUMBER_FROM_DOC_TYPE = {
    DocumentType.ID_CARD: "id_number",
    DocumentType.DRIVER_LICENSE: "license_number",
    DocumentType.RESIDENCE_PERMIT: "id_number",
    DocumentType.PASSPORT: "passport_number",
    DocumentType.HEALTH_INSURANCE_CARD: "health_insurance_number",
}
