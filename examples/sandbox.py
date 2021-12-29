import os
import random
import string
from typing import Optional

from meiga import isSuccess
from meiga.decorators import meiga

from alice import Config, Sandbox, UserInfo


@meiga
def sandbox_example(sandbox_token: str, email: str, verbose: Optional[bool] = False):
    config = Config(sandbox_token=sandbox_token, verbose=verbose)
    sandbox = Sandbox.from_config(config)

    user_id = sandbox.create_user(user_info=UserInfo(email=email)).unwrap_or_throw()
    user_token = sandbox.get_user_token(email=email).unwrap_or_throw()
    user = sandbox.get_user(email=email).unwrap_or_throw()
    sandbox.delete_user(email=email).unwrap_or_throw()

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
