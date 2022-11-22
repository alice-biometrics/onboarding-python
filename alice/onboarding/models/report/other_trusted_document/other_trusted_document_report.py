from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, Field

from alice.onboarding.models.report.other_trusted_document.other_trusted_document_report_meta import (
    OtherTrustedDocumentReportMeta,
)
from alice.onboarding.models.report.shared.href import Href


class OtherTrustedDocumentReport(BaseModel):
    """
    A other trusted document report_v1 collects all the information extracted for a document during the onboarding process
    """

    id: str = Field(
        description="Unique identifier (UUID v4 standard)",
        min_length=16,
        max_length=36,
    )
    created_at: datetime = Field(description="Creation time in ISO 8601 format")
    media: Dict[str, Optional[Href]] = Field(
        description="Other trusted document media resources"
    )

    meta: OtherTrustedDocumentReportMeta
