from typing import Optional

from alice.onboarding.models.report.checks.check import Check


class UnexpiredDocumentCheck(Check):
    def __init__(self, value: Optional[float] = None):
        super().__init__(
            key="unexpired_document", detail="The document has not expired", value=value
        )
