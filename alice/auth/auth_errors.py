from __future__ import annotations

from dataclasses import dataclass

from meiga import Error
from requests import Response


@dataclass
class AuthError(Error):
    operation: str
    code: int
    message: dict[str, str] | None  # type: ignore

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"[AuthError: [operation: {self.operation} | code: {self.code} | message: {self.message}]]"

    @staticmethod
    def from_response(operation: str, response: Response) -> AuthError:
        code = response.status_code
        try:
            message = response.json()
        except Exception:
            message = {"message": "no content"}
        return AuthError(operation=operation, code=code, message=message)
