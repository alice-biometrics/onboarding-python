import os
import string
import random

from meiga import isSuccess
from meiga.decorators import meiga

from alice import Sandbox, Config, UserInfo


@meiga
def sandbox_example(sandbox_token: str, email: str, verbose: bool = False):
    config = Config(sandbox_token=sandbox_token)
    sandbox = Sandbox.from_config(config)

    user_id = sandbox.create_user(
        user_info=UserInfo(email=email), verbose=verbose
    ).unwrap_or_return()
    user_token = sandbox.get_user_token(email=email, verbose=verbose).unwrap_or_return()
    user = sandbox.get_user(email=email, verbose=verbose).unwrap_or_return()
    sandbox.delete_user(email=email, verbose=verbose).unwrap_or_return()

    if verbose:
        print(f"user_id: {user_id}")
        print(f"user_token: {user_token}")
        print(f"user: {user}")

    return isSuccess


def random_mail():
    user = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    return f"example_{user}@alicebiometrics.com"


if __name__ == "__main__":
    sandbox_token = os.environ.get("ONBOARDING_SANDBOX_TOKEN")
    if sandbox_token is None:
        raise AssertionError(
            "Please configure your ONBOARDING_SANDBOX_TOKEN to run the example"
        )
    print("Running sandbox example...")
    sandbox_example(sandbox_token=sandbox_token, email=random_mail(), verbose=False)
