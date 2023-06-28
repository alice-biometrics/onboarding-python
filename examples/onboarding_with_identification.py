import os
from typing import Optional

from alice import Config, Onboarding

RESOURCES_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/../resources"


def identification_onboarding(api_key: str, verbose: Optional[bool] = False) -> None:

    config = Config(api_key=api_key, verbose=verbose)
    onboarding = Onboarding.from_config(config)

    selfie_media_data = given_any_selfie_image_media_data()
    document_front_media_data = given_any_document_front_media_data()

    user_id_target = onboarding.create_user().unwrap_or_throw()

    # Upload a selfie (Recommended 1-second video)
    onboarding.add_selfie(
        user_id=user_id_target, media_data=selfie_media_data
    ).unwrap_or_throw()

    user_id_probe = onboarding.create_user().unwrap_or_throw()

    onboarding.add_selfie(
        user_id=user_id_probe, media_data=document_front_media_data
    ).unwrap_or_throw()

    identifications = onboarding.identify_user(
        target_user_id=user_id_target, probe_user_ids=[user_id_probe, user_id_target]
    )
    assert isinstance(identifications.unwrap(), dict)


def given_any_selfie_image_media_data() -> bytes:
    with open(f"{RESOURCES_PATH}/selfie.png", "rb") as f:
        return f.read()


def given_any_document_front_media_data() -> bytes:
    with open(f"{RESOURCES_PATH}/idcard_esp_front_example.png", "rb") as f:
        return f.read()


def given_any_document_back_media_data() -> bytes:
    with open(f"{RESOURCES_PATH}/idcard_esp_back_example.png", "rb") as f:
        return f.read()


if __name__ == "__main__":
    api_key = os.environ.get("ONBOARDING_API_KEY")
    if api_key is None:
        raise AssertionError(
            "Please configure your ONBOARDING_API_KEY to run the example"
        )
    print("Running onboarding example...")
    identification_onboarding(api_key=api_key, verbose=True)
