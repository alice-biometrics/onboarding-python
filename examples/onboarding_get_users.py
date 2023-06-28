import os
from typing import Optional

from alice import Config, Onboarding


def onboarding_get_users_status_example(
    api_key: str, verbose: Optional[bool] = False
) -> None:
    config = Config(api_key=api_key, verbose=verbose)
    onboarding = Onboarding.from_config(config)

    onboarding.get_users().unwrap_or_throw()
    onboarding.get_users_status().unwrap_or_throw()


if __name__ == "__main__":
    api_key = os.environ.get("ONBOARDING_API_KEY")
    if api_key is None:
        raise AssertionError(
            "Please configure your ONBOARDING_API_KEY to run the example"
        )
    print("Running onboarding example...")
    onboarding_get_users_status_example(api_key=api_key, verbose=True)
