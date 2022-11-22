from datetime import datetime
from typing import Dict, List, Optional

from meiga import Error, Result, Success, isFailure
from pydantic import Field
from pydantic.main import BaseModel

from alice.onboarding.models.report.checks.check import Check
from alice.onboarding.models.report.shared.href import Href


class SelfieReport(BaseModel):
    """
    A selfie report_v1 collects all the information extracted for a selfie during the onboarding process
    """

    id: str = Field(
        description="Unique selfie identifier (UUID v4 standard)",
        min_length=16,
        max_length=36,
    )
    created_at: datetime = Field(description="Selfie creation time in ISO 8601 format")
    checks: List[Check] = Field(default=[], description="Selfie-level checks")
    liveness: Optional[float] = Field(
        ...,
        ge=0,
        le=100,
        description="Analysis to detect if the selfie is from a real person. The recommended threshold is 50.",
    )
    voided: bool = Field(description="Whether the selfie has been voided or not")
    media: Dict[str, Href] = Field(description="Selfie media resources")
    number_of_faces: Optional[int] = Field(
        description="Number of faces detected in the selfie"
    )

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
