from typing import Any, Dict, Optional

from pydantic import BaseModel
from requests import Response


class SandboxError(BaseModel):
    operation: str
    code: int
    message: Optional[Dict[str, Any]] = None

    def __repr__(self):
        return f"[SandboxError: [operation: {self.operation} | code: {self.code} | message: {self.message}]]"

    @staticmethod
    def from_response(operation: str, response: Response):
        code = response.status_code
        try:
            message = response.json()
        except:  # noqa E722
            message = {"message": "no content"}
        return SandboxError(operation=operation, code=code, message=message)
