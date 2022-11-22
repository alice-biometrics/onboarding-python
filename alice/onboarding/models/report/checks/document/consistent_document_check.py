from typing import Optional

from alice.onboarding.models.report.checks.check import Check


class ConsistentDocumentCheck(Check):
    _inconsistent_fields_th: int = 2

    def __init__(self, value: Optional[float] = None):
        super().__init__(
            key="consistent_document",
            detail=f"There are less than {self._inconsistent_fields_th} inconsistent fields between the document sides",
            value=value,
        )
