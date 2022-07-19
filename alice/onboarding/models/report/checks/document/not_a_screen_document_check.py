from typing import Optional

from alice.onboarding.models.report.checks.check import Check


class NotAScreenDocumentCheck(Check):
    def __init__(self, value: Optional[float] = None):
        super().__init__(
            key="not_a_screen_document",
            detail="The document's pictures are not taken from a screen",
            value=value,
        )
