from typing import Optional

from alice.onboarding.models.report.checks.check import Check


class ConsistentFieldCheck(Check):
    def __init__(self, value: Optional[float] = None):
        super().__init__(
            key="consistent_field",
            detail="The same field has the same value in other doc side",
            value=value,
        )
