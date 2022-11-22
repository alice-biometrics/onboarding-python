from typing import Optional

from alice.onboarding.models.report.checks.check import Check


class UnexpiredDateCheck(Check):
    def __init__(self, value: Optional[float] = None):
        super().__init__(
            key="unexpired_date", detail="Date has not expired", value=value
        )
