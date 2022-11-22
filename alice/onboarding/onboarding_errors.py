from typing import Any, Dict, Optional

from meiga import Error
from pydantic.dataclasses import dataclass
from requests import Response


@dataclass
class OnboardingError(Error):
    operation: str
    code: int
    message: Optional[Dict[str, Any]] = None

    def __init__(
        self, operation: str, code: int, message: Optional[Dict[str, Any]] = None
    ):
        self.operation = operation
        self.code = code
        self.message = message

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"[OnboardingError: [operation: {self.operation} | code: {self.code} | message: {self.message}]]"

    @staticmethod
    def from_response(operation: str, response: Response) -> "OnboardingError":
        code = response.status_code
        try:
            message = response.json()
        except Exception:
            message = {"message": "no content"}
        return OnboardingError(operation=operation, code=code, message=message)
