from datetime import datetime
from typing import Any, Dict, List, Optional

from meiga import Error, Result, Success, isFailure
from pydantic import Field
from pydantic.main import BaseModel

from alice.onboarding.models.report.document.document_field import ReportV1Field
from alice.onboarding.models.report.document.document_side import DocumentSide
from alice.onboarding.models.report.document.document_side_report_meta import (
    DocumentSideReportMeta,
)
from alice.onboarding.models.report.shared.href import Href


class DocumentSideReport(BaseModel):
    """
    It collects document metadata
    """

    side: DocumentSide
    fields: List[ReportV1Field] = Field(
        default=[], description="Document info extracted from side"
    )
    media: Dict[str, Optional[Href]] = Field(
        description="Document side media resources"
    )
    meta: DocumentSideReportMeta
    created_at: Optional[datetime]
    forensics_scores: Optional[Dict[str, Any]]

    def get_field(self, field_name: str) -> Result[ReportV1Field, Error]:
        for side_field in self.fields:
            if field_name == side_field.name:
                return Success(side_field)
        return isFailure

    def has_field(self, field_name: str) -> bool:
        return any([field_name == side_field.name for side_field in self.fields])

    def add_field(self, field: ReportV1Field) -> None:
        if not self.has_field(field.name):
            self.fields.append(field)

    def update_field(self, field: ReportV1Field) -> None:
        self.fields[:] = [
            field if field.name == side_field.name else side_field
            for side_field in self.fields
        ]
