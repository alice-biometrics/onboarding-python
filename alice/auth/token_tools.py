import time
from typing import Union
from unittest.mock import Mock

import jwt
from requests import Response


def is_valid_token(token: Union[str, None], margin_seconds: int = 60) -> bool:
    if not token:
        return False
    decoded_token = jwt.decode(token, options={"verify_signature": False})
    return bool(decoded_token["exp"] > time.time() - margin_seconds)


def get_token_from_response(response: Response) -> str:
    return response.json().get("token")  # type: ignore


def get_reponse_from_token(token: str) -> Response:
    response = Mock(spec=Response)
    response.json.return_value = {"token": token}
    response.status_code = 200
    return response
