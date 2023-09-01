import os
from typing import Optional

from requests import Response

from alice import Config, Onboarding
from alice.onboarding.models.ad_hoc_executor import AdHocExecutor


def onboarding_ad_hoc(api_key: str, verbose: Optional[bool] = False) -> None:
    config = Config(api_key=api_key, verbose=verbose)
    onboarding = Onboarding.from_config(config)

    # Create User (Backend without user_id)
    def create_user(executor: AdHocExecutor) -> Response:
        return executor.post_with(url_path="user")

    response = onboarding.ad_hoc(create_user).unwrap_or_raise()
    user_id = response.json().get("user_id")
    print(f"{user_id=}")

    # Get User State (Backend with user_id)
    def get_user_state(executor: AdHocExecutor) -> Response:
        return executor.get_with(url_path="/user/state")

    response = onboarding.ad_hoc(get_user_state, user_id=user_id).unwrap_or_raise()
    state = response.json()
    print(f"{state=}")


if __name__ == "__main__":
    api_key = os.environ.get("ONBOARDING_API_KEY")
    if api_key is None:
        raise AssertionError(
            "Please configure your ONBOARDING_API_KEY to run the example"
        )
    print("Running onboarding example...")
    onboarding_ad_hoc(api_key=api_key, verbose=True)
