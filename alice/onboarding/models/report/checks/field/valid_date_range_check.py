from typing import Optional

from alice.onboarding.models.report.checks.check import Check


class ValidDateRangeCheck(Check):
    def __init__(self, value: Optional[float] = None):
        super().__init__(
            key="valid_date_range", detail="Date is within valid range", value=value
        )
