import os

from meiga import isSuccess
from meiga.decorators import meiga

from alice import Onboarding, Config

RESOURCES_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/../resources"


@meiga
def identification_onboarding(api_key: str, verbose: bool = False):

    config = Config(api_key=api_key, verbose=verbose)
    onboarding = Onboarding.from_config(config)

    selfie_media_data = given_any_selfie_image_media_data()
    document_front_media_data = given_any_document_front_media_data()

    user_id_target = onboarding.create_user().unwrap_or_return()

    # Upload a selfie (Recommended 1-second video)
    onboarding.add_selfie(
        user_id=user_id_target, media_data=selfie_media_data
    ).unwrap_or_return()

    user_id_probe = onboarding.create_user().unwrap_or_return()

    onboarding.add_selfie(
        user_id=user_id_probe, media_data=document_front_media_data
    ).unwrap_or_return()

    identifications = onboarding.identify_user(
        target_user_id=user_id_target, probe_user_ids=[user_id_probe, user_id_target]
    )
    assert isinstance(identifications.unwrap(), dict)

    return isSuccess


def given_any_selfie_image_media_data():
    return open(f"{RESOURCES_PATH}/selfie.png", "rb").read()


def given_any_document_front_media_data():
    return open(f"{RESOURCES_PATH}/idcard_esp_front_example.png", "rb").read()


def given_any_document_back_media_data():
    return open(f"{RESOURCES_PATH}/idcard_esp_back_example.png", "rb").read()


if __name__ == "__main__":
    api_key = os.environ.get("ONBOARDING_API_KEY")
    if api_key is None:
        raise AssertionError(
            "Please configure your ONBOARDING_API_KEY to run the example"
        )
    print("Running onboarding example...")
    identification_onboarding(api_key=api_key, verbose=True)
