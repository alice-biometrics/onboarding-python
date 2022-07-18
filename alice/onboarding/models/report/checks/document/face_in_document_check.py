from typing import Optional

from alice.onboarding.models.report.checks.check import Check


class FaceInFrontSideDocumentCheck(Check):
    def __init__(self, value: Optional[float] = None):
        super().__init__(
            key="face_in_front_side",
            detail="The doc contains a face in its front side",
            value=value,
        )
