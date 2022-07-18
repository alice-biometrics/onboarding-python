from typing import Optional

from alice.onboarding.models.report_v1.checks.check import Check


class ExpectedFieldCheck(Check):
    def __init__(self, value: Optional[float] = None):
        super().__init__(
            key="expected_field",
            detail="The field matches what is expected",
            value=value,
        )
