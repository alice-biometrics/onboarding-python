from datetime import datetime
from typing import List, Union

from meiga import Error, Result, Success, isFailure
from pydantic import Field
from pydantic.main import BaseModel

from alice.onboarding.models.report.checks.check import Check
from alice.onboarding.models.report.document.document_field import ReportV1Field
from alice.onboarding.models.report.document.document_report_meta import (
    DocumentReportMeta,
)
from alice.onboarding.models.report.document.document_side_report import (
    DocumentSideReport,
)


class DocumentSidesDetailReport(BaseModel):
    front: Union[DocumentSideReport, None] = None
    back: Union[DocumentSideReport, None] = None
    internal: Union[DocumentSideReport, None] = None

    def get_completed_sides(self) -> int:
        completed_sides = 0
        if self.front:
            completed_sides += 1
        if self.back:
            completed_sides += 1
        if self.internal:
            completed_sides += 1
        return completed_sides


class DocumentReport(BaseModel):
    """
    A document report_v1 collects all the information extracted for a document during the onboarding process
    """

    id: str = Field(
        description="Unique document identifier (UUID v4 standard)",
        min_length=16,
        max_length=36,
    )
    created_at: datetime = Field(
        description="Document creation time in ISO 8601 format"
    )
    checks: List[Check] = Field(default=[], description="Document-level checks")
    summary_fields: List[ReportV1Field] = Field(
        default=[], description="Best-read document info from all its sides"
    )
    sides: DocumentSidesDetailReport = DocumentSidesDetailReport()
    meta: DocumentReportMeta

    def get_field(self, field_name: str) -> Result[ReportV1Field, Error]:
        for summary_field in self.summary_fields:
            if field_name == summary_field.name:
                return Success(summary_field)
        return isFailure

    def has_field(self, field_name: str) -> bool:
        return any(
            [field_name == summary_field.name for summary_field in self.summary_fields]
        )

    def add_field(self, field: ReportV1Field) -> None:
        if not self.has_field(field.name):
            self.summary_fields.append(field)

    def update_field(self, field: ReportV1Field) -> None:
        self.summary_fields[:] = [
            field if field.name == summary_field.name else summary_field
            for summary_field in self.summary_fields
        ]

    def get_check(self, check_key: str) -> Result[Check, Error]:
        for doc_check in self.checks:
            if check_key == doc_check.key:
                return Success(doc_check)
        return isFailure

    def has_check(self, check: Check) -> bool:
        return any(
            [
                check.key == field_check.key and check.value == field_check.value
                for field_check in self.checks
            ]
        )

    def add_check(self, check: Check) -> None:
        if not self.has_check(check):
            self.checks.append(check)
