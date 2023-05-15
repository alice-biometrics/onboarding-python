import os
from typing import Optional

from meiga import isSuccess
from meiga.decorators import meiga

from alice import Config, Onboarding
from alice.onboarding.enums.match_case import MatchCase

RESOURCES_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/../resources"


@meiga
def onboarding_with_user_matching(api_key: str, verbose: Optional[bool] = False):

    config = Config(api_key=api_key, verbose=verbose)
    onboarding = Onboarding.from_config(config)

    selfie_media_data = given_any_selfie_image_media_data()

    user_id = onboarding.create_user().unwrap_or_throw()

    # Upload a selfie (Recommended 1-second video)
    onboarding.add_selfie(
        user_id=user_id, media_data=selfie_media_data
    ).unwrap_or_throw()

    onboarding.void_selfie(user_id=user_id).unwrap_or_throw()

    onboarding.add_selfie(
        user_id=user_id, media_data=selfie_media_data
    ).unwrap_or_throw()

    matches = onboarding.user_matching(user_id=user_id, match_case=MatchCase.SELFIE)
    assert isinstance(matches.unwrap(), list)

    return isSuccess


def given_any_selfie_image_media_data():
    return open(f"{RESOURCES_PATH}/selfie.png", "rb").read()


if __name__ == "__main__":
    api_key = os.environ.get("ONBOARDING_API_KEY")
    if api_key is None:
        raise AssertionError(
            "Please configure your ONBOARDING_API_KEY to run the example"
        )
    print("Running onboarding example...")
    onboarding_with_user_matching(api_key=api_key, verbose=True)
