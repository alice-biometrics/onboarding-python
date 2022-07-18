from typing import Optional

from alice.onboarding.models.report_v1.checks.check import Check


class AuthenticNfcChipCheck(Check):
    def __init__(self, value: Optional[float] = None):
        super().__init__(
            key="authentic_nfc_chip",
            detail="The document's NFC is signed by an official authority. It has not been tampered nor cloned.",
            value=value,
        )
