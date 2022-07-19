from typing import Optional

from alice.onboarding.models.report.checks.check import Check


class ValidDateFormatCheck(Check):
    def __init__(self, value: Optional[float] = None):
        super().__init__(
            key="valid_date_format", detail="Valid date format", value=value
        )
