import os
from typing import Optional

from alice import Config, Onboarding
from alice.onboarding.enums.document_side import DocumentSide
from alice.onboarding.enums.document_type import DocumentType
from alice.onboarding.enums.version import Version

RESOURCES_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/../resources"


def onboarding_example(api_key: str, verbose: Optional[bool] = False) -> None:
    config = Config(api_key=api_key, verbose=verbose)
    onboarding = Onboarding.from_config(config)

    selfie_media_data = given_any_selfie_image_media_data()
    document_front_media_data = given_any_document_front_media_data()
    document_back_media_data = given_any_document_back_media_data()

    user_id = onboarding.create_user().unwrap_or_raise()

    onboarding.get_user_status(user_id).unwrap_or_raise()

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
    ).unwrap_or_raise()
    onboarding.add_document(
        user_id=user_id,
        document_id=document_id,
        media_data=document_back_media_data,
        side=DocumentSide.BACK,
        manual=True,
    ).unwrap_or_raise()

    # Generate the report
    report = onboarding.create_report(
        user_id=user_id, version=Version.V1
    ).unwrap_or_raise()

    if verbose:
        print(f"report: {report}")

    href = report.selfies[0].media.get("cropped_face").href
    media = onboarding.download(user_id=user_id, href=href).unwrap_or_raise()
    assert isinstance(media, bytes)

    # Enable authentication for a user
    # Based on report results and your business logic, you can enable the authentication for a user
    onboarding.enable_authentication(user_id=user_id).unwrap_or_raise()

    # Authenticate a user (only available if a user is already authorized)
    onboarding.authenticate_user(
        user_id=user_id, media_data=selfie_media_data
    ).unwrap_or_raise()


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
    onboarding_example(api_key=api_key, verbose=True)
