import os

from meiga import isSuccess
from meiga.decorators import meiga

from alice import Onboarding, Config

RESOURCES_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/../resources"


@meiga
def certified_onboarding(api_key: str, verbose: bool = False):

    config = Config(api_key=api_key, verbose=verbose)
    onboarding = Onboarding.from_config(config)

    selfie_media_data = given_any_selfie_image_media_data()
    document_front_media_data = given_any_document_front_media_data()
    document_back_media_data = given_any_document_back_media_data()

    user_id = onboarding.create_user().unwrap_or_return()

    # Upload a selfie (Recommended 1-second video)
    onboarding.add_selfie(
        user_id=user_id, media_data=selfie_media_data
    ).unwrap_or_return()

    # Create and upload front and back side from a document
    document_id = onboarding.create_document(
        user_id=user_id, type="idcard", issuing_country="ESP"
    ).unwrap_or_return()
    onboarding.add_document(
        user_id=user_id,
        document_id=document_id,
        media_data=document_front_media_data,
        side="front",
        manual=True,
    ).unwrap_or_return()
    onboarding.add_document(
        user_id=user_id,
        document_id=document_id,
        media_data=document_back_media_data,
        side="back",
        manual=True,
    ).unwrap_or_return()

    # Create Certificate
    certificate_id = onboarding.create_certificate(user_id=user_id).unwrap_or_return()

    # Retrieved Certificate from certificate_id
    certificate = onboarding.retrieve_certificate(
        user_id=user_id, certificate_id=certificate_id
    ).unwrap_or_return()

    # Save PdfReport data to a file
    with open(f"certificate_{certificate_id}.pdf", "wb") as outfile:
        outfile.write(certificate)

    certificates = onboarding.retrieve_certificates(user_id=user_id).unwrap_or_return()

    assert len(certificates) >= 1

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
    print("Running onboarding with certificate example...")
    certified_onboarding(api_key=api_key, verbose=False)
