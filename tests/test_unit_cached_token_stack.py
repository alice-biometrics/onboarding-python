from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
import pytest

from alice.auth.cached_token_stack import CachedTokenStack


def generate_dummy_token(
    expired: bool = False, payload_value: str = "payload_value"
) -> str:
    if expired:
        exp = (datetime.now(timezone.utc) - timedelta(minutes=60)).timestamp()
    else:
        exp = (datetime.now(timezone.utc) + timedelta(minutes=60)).timestamp()

    encoded_jwt = jwt.encode(
        {"id": payload_value, "exp": exp}, "secret", algorithm="HS256"
    )
    return encoded_jwt


@pytest.mark.unit
class TestCachedTokenStack:
    def setup_method(self):
        self.user_id = str(uuid4())

    def should_add_and_get_a_token(self):
        stack = CachedTokenStack()

        token = generate_dummy_token()
        stack.add("key", token)
        retrieved_token = stack.get("key")

        assert token == retrieved_token

    def should_keep_max_size(self):
        stack = CachedTokenStack(max_size=3)

        for i in range(6):
            stack.add(
                str(i), generate_dummy_token(payload_value=f"payload_value_{str(i)}")
            )

        token = stack.get("1")  # this forces clear

        assert len(stack) == 3

    def should_remove_expired_tokens(self):
        stack = CachedTokenStack()

        for i in range(4):
            stack._data[str(i)] = generate_dummy_token(
                payload_value=f"payload_value_{str(i)}", expired=True
            )

        assert len(stack) == 4

        for i in range(6, 12):
            stack.add(
                str(i), generate_dummy_token(payload_value=f"payload_value_{str(i)}")
            )

        token = stack.get(
            "not_available_user_id"
        )  # this will not forces clear since there is no cached token
        assert len(stack) == 10

        token = stack.get(str(i))  # this forces clear
        assert len(stack) == 6
