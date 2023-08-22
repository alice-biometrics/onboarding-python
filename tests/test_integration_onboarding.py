import pytest
from meiga import Error, Result, Success, early_return

from alice import Config, DeviceInfo, Onboarding, UserInfo
from alice.auth.auth_errors import AuthError
from alice.onboarding.enums.document_side import DocumentSide
from alice.onboarding.enums.document_source import DocumentSource
from alice.onboarding.enums.document_type import DocumentType
from alice.onboarding.enums.user_state import UserState
from alice.onboarding.enums.version import Version
from alice.onboarding.models.report.report import Report


@pytest.mark.unit
def test_should_return_an_error_when_the_api_key_is_not_configured():

    config = Config()
    onboarding = Onboarding.from_config(config)

    result = onboarding.create_user()

    result.assert_failure()


@pytest.mark.unit
def test_should_timeout_when_time_exceeded(
    given_valid_api_key, given_any_selfie_image_media_data
):
    config = Config(api_key=given_valid_api_key, timeout=0.1)
    onboarding = Onboarding.from_config(config)

    result = onboarding.create_user(
        user_info=UserInfo(first_name="Alice", last_name="Biometrics"),
        device_info=DeviceInfo(device_platform="Android"),
    )
    result.assert_failure(value_is_instance_of=AuthError)
    assert result.value.code == 408


@pytest.mark.unit
def test_should_do_complete_onboarding_process(
    given_valid_api_key,
    given_any_selfie_image_media_data,
    given_any_document_front_media_data,
    given_any_document_back_media_data,
    given_any_pdf_media_data,
):
    @early_return
    def do_complete_onboarding() -> Result[dict, Error]:
        config = Config(api_key=given_valid_api_key)
        onboarding = Onboarding.from_config(config)

        user_id = onboarding.create_user(
            user_info=UserInfo(first_name="Alice", last_name="Biometrics"),
            device_info=DeviceInfo(device_platform="Android"),
        ).unwrap_or_return()
        onboarding.add_selfie(
            user_id=user_id, media_data=given_any_selfie_image_media_data
        ).unwrap_or_return()
        document_id = onboarding.create_document(
            user_id=user_id, type=DocumentType.ID_CARD, issuing_country="ESP"
        ).unwrap_or_return()
        onboarding.document_properties(
            user_id=user_id, type=DocumentType.ID_CARD, issuing_country="ESP"
        ).unwrap_or_return()
        onboarding.add_document(
            user_id=user_id,
            document_id=document_id,
            media_data=given_any_document_front_media_data,
            side=DocumentSide.FRONT,
            manual=True,
            source=DocumentSource.camera,
        ).unwrap_or_return()
        onboarding.add_document(
            user_id=user_id,
            document_id=document_id,
            media_data=given_any_document_back_media_data,
            side=DocumentSide.BACK,
            manual=True,
            source=DocumentSource.camera,
        ).unwrap_or_return()
        onboarding.add_other_trusted_document(
            user_id=user_id, pdf=given_any_pdf_media_data
        ).unwrap_or_return()
        report = onboarding.create_report(
            user_id=user_id, version=Version.V1
        ).unwrap_or_return()

        certificate_id = onboarding.create_certificate(
            user_id=user_id
        ).unwrap_or_return()

        onboarding.retrieve_certificate(
            user_id=user_id, certificate_id=certificate_id
        ).unwrap_or_return()

        onboarding.retrieve_certificates(user_id=user_id).unwrap_or_return()

        onboarding.update_user_state(
            user_id=user_id, user_state=UserState.TO_REVIEW
        ).unwrap_or_return()
        onboarding.update_user_state(
            user_id=user_id, user_state=UserState.ACCEPTED
        ).unwrap_or_return()
        onboarding.update_user_state(
            user_id=user_id, user_state=UserState.REJECTED
        ).unwrap_or_return()

        user_state = onboarding.get_user_state(user_id=user_id).unwrap_or_return()
        assert user_state == UserState.REJECTED

        onboarding.delete_user(user_id).unwrap_or_return()

        return Success(report)

    result = do_complete_onboarding()

    result.assert_success(value_is_instance_of=Report)
