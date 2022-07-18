from typing import Optional

from alice.onboarding.models.report_v1.checks.check import Check


class CheckedInfoCodeCheck(Check):
    def __init__(self, value: Optional[float] = None):
        super().__init__(
            key="checked_info_code",
            detail="The document's MRZ/PDF417/QR is checked",
            value=value,
        )
