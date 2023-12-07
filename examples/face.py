import os
from typing import Optional

from alice import Config, Face

RESOURCES_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/../resources"


def face_example(api_key: str, verbose: Optional[bool] = False) -> None:
    config = Config(api_key=api_key, verbose=verbose)
    face = Face.from_config(config)

    selfie_media_data = given_any_selfie_image_media_data()
    document_front_media_data = given_any_document_front_media_data()

    selfie_result = face.selfie(selfie_media_data).unwrap_or_raise()

    document_result = face.document(document_front_media_data).unwrap_or_raise()

    match_result = face.match_profiles(
        selfie_result.face_profile, document_result.face_profile
    ).unwrap_or_raise()
    print(match_result)


def given_any_selfie_image_media_data() -> bytes:
    with open(f"{RESOURCES_PATH}/selfie.png", "rb") as f:
        return f.read()


def given_any_document_front_media_data() -> bytes:
    with open(f"{RESOURCES_PATH}/idcard_esp_front_example.png", "rb") as f:
        return f.read()


if __name__ == "__main__":
    api_key = os.environ.get("ONBOARDING_API_KEY")
    if api_key is None:
        raise AssertionError(
            "Please configure your ONBOARDING_API_KEY to run the example"
        )
    print("Running face example...")
    face_example(api_key=api_key, verbose=True)
