from typing import List, Optional

from meiga import Error, Result, Success, isFailure
from pydantic.main import BaseModel

from alice.onboarding.models.report.checks.check import Check


class ReportV1Field(BaseModel):
    """
    It collects the extracted OCR info
    """

    name: str
    value: Optional[str]
    score: Optional[int]
    checks: List[Check] = []

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

    def has_critical_checks(self) -> bool:
        from alice.onboarding.models.report.checks.field.valid_date_format_check import (
            ValidDateFormatCheck,
        )
        from alice.onboarding.models.report.checks.field.valid_date_range_check import (
            ValidDateRangeCheck,
        )

        critical_checks = [
            ValidDateFormatCheck(value=0.0),
            ValidDateRangeCheck(value=0.0),
        ]  # IncompleteNameAlert
        return any(
            [self.has_check(critical_check) for critical_check in critical_checks]
        )

    def is_checked(self) -> bool:  # has CheckedFieldCheck to True
        from alice.onboarding.models.report.checks.field.cheked_field_check import (
            CheckedFieldCheck,
        )

        return self.has_check(CheckedFieldCheck(value=100.0))

    def is_valid(self) -> bool:
        if self.value is None:
            return False
        else:
            return not self.has_critical_checks()
