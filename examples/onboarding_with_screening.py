import os
from typing import Optional

from alice import Config, Onboarding, UserInfo
from alice.onboarding.enums.document_side import DocumentSide
from alice.onboarding.enums.document_type import DocumentType

RESOURCES_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/../resources"


def screening_onboarding(api_key: str, verbose: Optional[bool] = False) -> None:
    config = Config(api_key=api_key, verbose=verbose)
    onboarding = Onboarding.from_config(config)

    document_back_media_data = given_any_document_back_media_data()

    user_id = onboarding.create_user(
        user_info=UserInfo(first_name="Carmen", last_name="Espanola")
    ).unwrap_or_raise()

    # # Create and upload front and back side from a document
    document_id = onboarding.create_document(
        user_id=user_id, type=DocumentType.ID_CARD, issuing_country="ESP"
    ).unwrap_or_raise()
    onboarding.add_document(
        user_id=user_id,
        document_id=document_id,
        media_data=document_back_media_data,
        side=DocumentSide.BACK,
        manual=True,
    ).unwrap_or_raise()

    # Screening
    screening = onboarding.screening(user_id=user_id).unwrap_or_raise()

    assert isinstance(screening, dict)

    # Screening (with detail)
    detailed_screening = onboarding.screening(
        user_id=user_id, detail=True
    ).unwrap_or_raise()
    assert isinstance(detailed_screening, dict)

    # Add user to monitoring list
    onboarding.screening_monitor_add(user_id=user_id).unwrap_or_raise()

    open_alerts = onboarding.screening_monitor_open_alerts().unwrap_or_raise()
    assert isinstance(open_alerts, dict)

    onboarding.screening_monitor_delete(
        user_id=user_id, verbose=verbose
    ).unwrap_or_raise()


def given_any_document_back_media_data() -> bytes:
    with open(f"{RESOURCES_PATH}/idcard_esp_back_example.png", "rb") as f:
        return f.read()


if __name__ == "__main__":
    api_key = os.environ.get("ONBOARDING_API_KEY")
    if api_key is None:
        raise AssertionError(
            "Please configure your ONBOARDING_API_KEY to run the example"
        )
    print("Running onboarding with screening example...")
    screening_onboarding(api_key=api_key, verbose=True)
