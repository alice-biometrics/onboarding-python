from typing import Optional

from pydantic import BaseModel, Field


class OtherTrustedDocumentReportMeta(BaseModel):
    """
    It collects other trusted document metadata
    """

    voided: bool = Field(description="Whether the doc has been voided or not")
    category: Optional[str] = Field(
        default=None, description="Defines the category of the document"
    )
