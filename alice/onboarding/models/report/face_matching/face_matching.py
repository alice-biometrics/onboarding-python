from datetime import datetime

from pydantic import Field
from pydantic.main import BaseModel

from alice.onboarding.models.report.document.document_side import DocumentSide


class FaceMatchingMeta(BaseModel):
    """
    Face matching metadata
    """

    document_id: str = Field(
        description="Unique document identifier (UUID v4 standard)",
        min_length=16,
        max_length=36,
    )
    selfie_id: str = Field(
        description="Unique selfie identifier (UUID v4 standard)",
        min_length=16,
        max_length=42,
    )
    created_at: datetime = Field(
        description="Face match creation time in ISO 8601 format"
    )
    side: DocumentSide = Field(description="Document side")


class FaceMatching(BaseModel):
    """
    It analyses whether the document's face and selfie are from the same person
    """

    score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Face matching score. The recommended threshold is 50.",
    )
    meta: FaceMatchingMeta
