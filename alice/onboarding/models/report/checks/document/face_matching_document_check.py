from typing import Optional

from alice.onboarding.models.report.checks.check import Check


class FaceMatchingDocumentCheck(Check):
    def __init__(self, value: Optional[float] = None):
        super().__init__(
            key="face_matching",
            detail="The document and active selfie faces are from the same person",
            value=value,
        )
