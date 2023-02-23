from alice.auth.catched_token_stack import CachedTokenStack
from tests.test_unit_cached_token_stack import generate_dummy_token

stack = CachedTokenStack(max_size=10)

print(stack)

number_of_expired_tokens = 100
print(f"Adding {number_of_expired_tokens} expired tokens...")
for i in range(number_of_expired_tokens):
    stack.add(
        str(i),
        generate_dummy_token(payload_value=f"payload_value_{str(i)}", expired=True),
    )
print("Done")

print(stack)

number_valid_tokens = 1000
print(f"Adding {number_valid_tokens} valid tokens...")
for i in range(number_of_expired_tokens, number_valid_tokens):
    stack.add(str(i), generate_dummy_token(payload_value=f"payload_value_{str(i)}"))
print("Done")

print(stack)

stack.get("200")

stack.show()
