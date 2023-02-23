import json
import time
from typing import Union

import jwt
from requests import Response


def is_valid_token(token: Union[str, None], margin_seconds: int = 60) -> bool:
    if not token:
        return False
    decoded_token = jwt.decode(token, options={"verify_signature": False})
    return bool(decoded_token["exp"] > time.time() - margin_seconds)


def get_token_from_response(response: Response) -> str:
    response_json = json.loads(response.content)
    token: str = response_json["token"]
    return token
