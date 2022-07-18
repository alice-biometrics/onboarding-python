from typing import Optional

from alice.onboarding.models.report_v1.checks.check import Check


class Over18Check(Check):
    def __init__(self, value: Optional[float] = None):
        super().__init__(key="over_18", detail="Over 18 years old", value=value)
