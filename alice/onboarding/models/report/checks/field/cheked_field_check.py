from typing import Optional

from alice.onboarding.models.report.checks.check import Check


class CheckedFieldCheck(Check):
    def __init__(self, value: Optional[float] = None):
        super().__init__(
            key="checked_field", detail="The field passes its checksum", value=value
        )
