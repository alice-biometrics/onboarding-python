from typing import Optional

from alice.onboarding.models.report.checks.check import Check


class OnlyOneDeviceCheck(Check):
    def __init__(self, value: Optional[float] = None):
        super().__init__(
            key="only_one_device_check",
            detail="All information has been uploaded by the user with the same device",
            value=value,
        )
