from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from alice.onboarding.models.report.compliance.user_event_out import UserEventOut
from alice.onboarding.models.report.document.document_report import DocumentReport
from alice.onboarding.models.report.other_trusted_document.other_trusted_document_report import (
    OtherTrustedDocumentReport,
)
from alice.onboarding.models.report.selfie.selfie_report import SelfieReport
from alice.onboarding.models.report.summary.report_summary import ReportSummary


class Report(BaseModel):
    """
    A report collects all the information extracted for a user during the onboarding process
    """

    id: str = Field(
        description="Unique report identifier (UUID v4 standard)",
        min_length=16,
        max_length=36,
    )
    user_id: str = Field(
        description="Unique user identifier (UUID v4 standard)",
        min_length=16,
        max_length=36,
    )
    version: int = Field(default=1, description="Report version", const=True)
    created_at: datetime = Field(description="Report creation time in ISO 8601 format")
    summary: ReportSummary = Field(description="User summary")
    selfies: List[SelfieReport] = Field(description="It collects all user selfies")
    documents: List[DocumentReport] = Field(
        description="It collects all user documents"
    )
    other_trusted_documents: List[OtherTrustedDocumentReport] = Field(
        description="It collects all user other trusted documents (bank receipts, proof of address...)",
        default=[],
    )
    events: List[UserEventOut] = Field(description="It collects all user events")
