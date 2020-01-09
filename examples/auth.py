import os

from meiga import isSuccess
from meiga.decorators import meiga

from alice import Auth, Config


@meiga
def auth_example(api_key: str, user_id:str, verbose: bool = False):
    config = Config(api_key=api_key)
    auth = Auth.from_config(config)

    backend_token = auth.create_backend_token(verbose=verbose).handle()
    backend_token_with_user = auth.create_backend_token(user_id=user_id).handle()
    user_token = auth.create_user_token(user_id=user_id).handle()

    return isSuccess


if __name__ == "__main__":
    api_key = os.environ.get("ONBOARDING_API_KEY")
    if api_key is None:
        raise AssertionError(
            "Please configure your ONBOARDING_API_KEY to run the example"
        )

    user_id = os.environ.get("ONBOARDING_USER_ID")
    if user_id is None:
        raise AssertionError(
            "Please configure your ONBOARDING_USER_ID to run the example"
        )

    result = auth_example(
        api_key=api_key, user_id=user_id, verbose=True
    )

    print(result)
