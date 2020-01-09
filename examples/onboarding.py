from alice import Sandbox, UserInfo

sandbox_token_pre = "<ADD-HERE-YOUR-SANDBOX-TOKEN"

email = "python-playground@alicebiometrics.com"

sandbox_sdk = Sandbox(sandbox_token=sandbox_token_pre)

result = sandbox_sdk.healthcheck(verbose=True)
print(result)

result = sandbox_sdk.create_user(user_info=UserInfo(email=email), verbose=True)
print(result)

result = sandbox_sdk.get_user(email=email, verbose=True)
print(result)

result = sandbox_sdk.get_user_token(email=email, verbose=True)
print(result)

result = sandbox_sdk.delete_user(email=email, verbose=True)
print(result)
