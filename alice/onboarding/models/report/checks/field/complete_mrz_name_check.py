from typing import Optional

from alice.onboarding.models.report.checks.check import Check


class CompleteMrzNameCheck(Check):
    def __init__(self, value: Optional[float] = None):
        super().__init__(
            key="complete_mrz_name",
            detail="Name is entirely contained in MRZ",
            value=value,
        )
