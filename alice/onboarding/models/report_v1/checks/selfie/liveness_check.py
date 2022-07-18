from typing import Optional

from alice.onboarding.models.report_v1.checks.check import Check


class LivenessCheck(Check):
    def __init__(self, value: Optional[float] = None):
        super().__init__(
            key="liveness",
            detail="The selfie is from a real person",
            value=value,
        )
