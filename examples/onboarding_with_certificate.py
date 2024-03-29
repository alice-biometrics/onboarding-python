import os
from typing import Optional

from meiga import isSuccess

from alice import Config, Onboarding
from alice.onboarding.enums.document_side import DocumentSide
from alice.onboarding.enums.document_source import DocumentSource
from alice.onboarding.enums.document_type import DocumentType

RESOURCES_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/../resources"


def certified_onboarding(api_key: str, verbose: Optional[bool] = False) -> None:

    config = Config(api_key=api_key, verbose=verbose)
    onboarding = Onboarding.from_config(config)

    selfie_media_data = given_any_selfie_image_media_data()
    document_front_media_data = given_any_document_front_media_data()
    document_back_media_data = given_any_document_back_media_data()

    user_id = onboarding.create_user().unwrap_or_raise()

    # Upload a selfie (Recommended 1-second video)
    onboarding.add_selfie(
        user_id=user_id, media_data=selfie_media_data
    ).unwrap_or_raise()

    # Create and upload front and back side from a document
    document_id = onboarding.create_document(
        user_id=user_id, type=DocumentType.ID_CARD, issuing_country="ESP"
    ).unwrap_or_raise()
    onboarding.add_document(
        user_id=user_id,
        document_id=document_id,
        media_data=document_front_media_data,
        side=DocumentSide.FRONT,
        manual=True,
        source=DocumentSource.camera,
    ).unwrap_or_raise()
    onboarding.add_document(
        user_id=user_id,
        document_id=document_id,
        media_data=document_back_media_data,
        side=DocumentSide.BACK,
        manual=True,
        source=DocumentSource.camera,
    ).unwrap_or_raise()

    # Create Certificate
    certificate_id = onboarding.create_certificate(user_id=user_id).unwrap_or_raise()

    # Retrieved Certificate from certificate_id
    certificate = onboarding.retrieve_certificate(
        user_id=user_id, certificate_id=certificate_id
    ).unwrap_or_raise()

    # Save PdfReport data to a file
    with open(f"certificate_{certificate_id}.pdf", "wb") as outfile:
        outfile.write(certificate)

    certificates = onboarding.retrieve_certificates(user_id=user_id).unwrap_or_raise()

    assert len(certificates) >= 1

    return isSuccess


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
    print("Running onboarding with certificate example...")
    certified_onboarding(api_key=api_key, verbose=False)
