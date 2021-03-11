import os

from meiga import Result, Error, isSuccess
from meiga.decorators import meiga

from alice import Auth, Config, Onboarding


@meiga
def get_user_id_from_onboarding(api_key, verbose: bool = False) -> Result[str, Error]:
    config = Config(api_key=api_key, verbose=verbose)
    onboarding = Onboarding.from_config(config)

    return onboarding.create_user()


@meiga
def auth_example(api_key: str, user_id: str, verbose: bool = False):
    config = Config(api_key=api_key, verbose=verbose)
    auth = Auth.from_config(config)

    backend_token = auth.create_backend_token().unwrap_or_return()
    backend_token_with_user = auth.create_backend_token(
        user_id=user_id
    ).unwrap_or_return()
    user_token = auth.create_user_token(user_id=user_id).unwrap_or_return()

    return isSuccess


if __name__ == "__main__":
    api_key = os.environ.get("ONBOARDING_API_KEY")
    if api_key is None:
        raise AssertionError(
            "Please configure your ONBOARDING_API_KEY to run the example"
        )
    verbose = False
    user_id = get_user_id_from_onboarding(
        api_key=api_key, verbose=verbose
    ).unwrap_or_throw()
    print("Running auth example...")
    auth_example(api_key=api_key, user_id=user_id, verbose=verbose)
