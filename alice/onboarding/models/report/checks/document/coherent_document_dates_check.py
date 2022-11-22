from typing import Optional

from alice.onboarding.models.report.checks.check import Check


class CoherentDocumentDatesCheck(Check):
    def __init__(self, value: Optional[float] = None):
        super().__init__(
            key="coherent_document_dates",
            detail="The document dates are coherent with each other",
            value=value,
        )
