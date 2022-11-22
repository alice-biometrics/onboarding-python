from typing import Optional

from alice.onboarding.models.report.checks.check import Check


class NotASyntheticDocumentCheck(Check):
    def __init__(self, value: Optional[float] = None):
        super().__init__(
            key="not_a_synthetic_document",
            detail="The document's pictures are not generated digitally",
            value=value,
        )
