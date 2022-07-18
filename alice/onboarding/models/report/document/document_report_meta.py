from pydantic import Field
from pydantic.main import BaseModel

from alice.onboarding.models.report.document.document_type import DocumentType


class DocumentReportMeta(BaseModel):
    """
    It collects document metadata
    """

    type: DocumentType
    issuing_country: str = Field(
        description="Document issuing country in ISO 3166-1 alpha-3 format"
    )
    completed: bool = Field(description="True if all document sides are captured")
    voided: bool = Field(description="Whether the doc has been voided or not")
