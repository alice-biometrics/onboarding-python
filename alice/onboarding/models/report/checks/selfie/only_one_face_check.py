from typing import Optional

from alice.onboarding.models.report.checks.check import Check


class OnlyOneFaceCheck(Check):
    def __init__(self, value: Optional[float] = None):
        super().__init__(
            key="only_one_face",
            detail="Only one face detected in the Selfie",
            value=value,
        )
