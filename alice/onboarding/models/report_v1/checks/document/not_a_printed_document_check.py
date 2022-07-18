from typing import Optional

from alice.onboarding.models.report_v1.checks.check import Check


class NotAPrintedDocumentCheck(Check):
    def __init__(self, value: Optional[float] = None):
        super().__init__(
            key="not_a_printed_document",
            detail="The document is not a print",
            value=value,
        )
