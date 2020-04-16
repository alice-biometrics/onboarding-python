from typing import Dict

from dataclasses import dataclass
from meiga import Error
from requests import Response


@dataclass
class OnboardingError(Error):
    operation: str
    code: int
    message: Dict[str, str]

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"[OnboardingError: [operation: {self.operation} | code: {self.code} | message: {self.message}]]"

    @staticmethod
    def from_response(operation: str, response: Response):
        code = response.status_code
        try:
            message = response.json()
        except Exception:
            message = {"message": "no content"}
        return OnboardingError(operation=operation, code=code, message=message)
