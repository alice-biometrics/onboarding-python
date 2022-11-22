from typing import Any, Dict, Optional

from meiga import Error
from pydantic.dataclasses import dataclass
from requests import Response


@dataclass
class SandboxError(Error):
    operation: str
    code: int
    message: Optional[Dict[str, Any]] = None

    def __init__(
        self, operation: str, code: int, message: Optional[Dict[str, Any]] = None
    ):
        self.operation = operation
        self.code = code
        self.message = message

    def __repr__(self) -> str:
        return f"[SandboxError: [operation: {self.operation} | code: {self.code} | message: {self.message}]]"

    @staticmethod
    def from_response(operation: str, response: Response) -> "SandboxError":
        code = response.status_code
        try:
            message = response.json()
        except:  # noqa E722
            message = {"message": "no content"}
        return SandboxError(operation=operation, code=code, message=message)
