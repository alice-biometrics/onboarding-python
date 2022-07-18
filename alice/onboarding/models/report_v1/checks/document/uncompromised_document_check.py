from typing import Optional

from alice.onboarding.models.report_v1.checks.check import Check


class UncompromisedDocumentCheck(Check):
    def __init__(self, value: Optional[float] = None):
        super().__init__(
            key="uncompromised_document",
            detail="The document has not been found in our internal database of compromised documents",
            value=value,
        )
