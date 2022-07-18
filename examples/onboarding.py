import os
from typing import Optional

from meiga import isSuccess
from meiga.decorators import meiga

from alice import Config, Onboarding
from alice.onboarding.enums.document_side import DocumentSide
from alice.onboarding.enums.document_type import DocumentType

RESOURCES_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/../resources"


@meiga
def onboarding_example(api_key: str, verbose: Optional[bool] = False):
    config = Config(api_key=api_key, verbose=verbose)
    onboarding = Onboarding.from_config(config)

    selfie_media_data = given_any_selfie_image_media_data()
    document_front_media_data = given_any_document_front_media_data()
    document_back_media_data = given_any_document_back_media_data()

    user_id = onboarding.create_user().unwrap_or_throw()

    # Upload a selfie (Recommended 1-second video)
    onboarding.add_selfie(
        user_id=user_id, media_data=selfie_media_data
    ).unwrap_or_throw()

    # Create and upload front and back side from a document
    document_id = onboarding.create_document(
        user_id=user_id, type=DocumentType.ID_CARD, issuing_country="ESP"
    ).unwrap_or_throw()
    onboarding.add_document(
        user_id=user_id,
        document_id=document_id,
        media_data=document_front_media_data,
        side=DocumentSide.FRONT,
        manual=True,
    ).unwrap_or_throw()
    onboarding.add_document(
        user_id=user_id,
        document_id=document_id,
        media_data=document_back_media_data,
        side=DocumentSide.BACK,
        manual=True,
    ).unwrap_or_throw()

    # Generate the report
    report = onboarding.create_report(user_id=user_id).unwrap_or_throw()

    if verbose:
        print(f"report: {report}")

    href = report.selfies[0].media.get("cropped_face").href
    media = onboarding.download(user_id=user_id, href=href).unwrap_or_throw()
    assert isinstance(media, bytes)

    # Authorize an user
    # Based on report results and your business logic, you can authorize an user
    onboarding.authorize_user(user_id=user_id)

    # Authenticate an user (only available if a user is already authorized)
    onboarding.authenticate_user(user_id=user_id, media_data=selfie_media_data)

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
    onboarding_example(api_key=api_key, verbose=True)
