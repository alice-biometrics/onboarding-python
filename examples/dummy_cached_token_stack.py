from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt

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


stack = CachedTokenStack(max_size=100)

print(stack)

number_of_expired_tokens = 100
print(f"Adding {number_of_expired_tokens} expired tokens...")
for i in range(number_of_expired_tokens):
    stack.add(
        str(uuid4()),
        generate_dummy_token(payload_value=f"payload_value_{str(i)}", expired=True),
    )
print("Done")

print(stack)

number_valid_tokens = 5000
print(f"Adding {number_valid_tokens} valid tokens...")
for i in range(number_of_expired_tokens, number_valid_tokens):
    stack.add(
        str(uuid4()), generate_dummy_token(payload_value=f"payload_value_{str(i)}")
    )
print("Done")

user_id = str(uuid4())
stack.add(user_id, generate_dummy_token(payload_value=f"payload_value_{str(i+1)}"))

print(stack)

stack.get(user_id)

print(stack)
