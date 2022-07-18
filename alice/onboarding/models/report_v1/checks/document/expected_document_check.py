from typing import Optional

from alice.onboarding.models.report_v1.checks.check import Check


class ExpectedDocumentCheck(Check):
    def __init__(self, value: Optional[float] = None):
        super().__init__(
            key="expected_document",
            detail="Read and selected documents match",
            value=value,
        )
