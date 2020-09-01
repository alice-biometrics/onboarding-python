import os

from meiga import isSuccess
from meiga.decorators import meiga

from alice import Onboarding, Config

RESOURCES_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/../resources"


@meiga
def screening_onboarding(api_key: str, verbose: bool = False):

    config = Config(api_key=api_key)

    config.onboarding_url = "https://pre.alicebiometrics.com/onboarding"
    config.sandbox_url = "https://pre.alicebiometrics.com/onboarding/sandbox"
    config.auth_url = "https://pre.alicebiometrics.com/auth"

    onboarding = Onboarding.from_config(config)

    selfie_media_data = given_any_selfie_image_media_data()
    document_front_media_data = given_any_document_front_media_data()
    document_back_media_data = given_any_document_back_media_data()

    user_id = onboarding.create_user(verbose=verbose).unwrap_or_return()

    # Upload a selfie (Recommended 1-second video)
    onboarding.add_selfie(
        user_id=user_id, media_data=selfie_media_data, verbose=verbose
    ).unwrap_or_return()

    # Create and upload front and back side from a document
    document_id = onboarding.create_document(
        user_id=user_id, type="idcard", issuing_country="ESP", verbose=verbose
    ).unwrap_or_return()
    onboarding.add_document(
        user_id=user_id,
        document_id=document_id,
        media_data=document_front_media_data,
        side="front",
        manual=True,
        verbose=verbose,
    ).unwrap_or_return()
    onboarding.add_document(
        user_id=user_id,
        document_id=document_id,
        media_data=document_back_media_data,
        side="back",
        manual=True,
        verbose=verbose,
    ).unwrap_or_return()

    # Screening
    screening = onboarding.screening(
        user_id=user_id, verbose=verbose
    ).unwrap_or_return()

    assert isinstance(screening, dict)

    # Screening (with detail)
    detailed_screening = onboarding.screening(
        user_id=user_id, detail=True, verbose=verbose
    ).unwrap_or_return()
    assert isinstance(detailed_screening, dict)
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
    print("Running onboarding with screening example...")
    screening_onboarding(api_key=api_key, verbose=True)
