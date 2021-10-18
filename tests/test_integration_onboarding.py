from typing import Dict

from meiga import Error, Result, Success
from meiga.assertions import assert_failure, assert_success
from meiga.decorators import meiga

from alice import Config, Onboarding


def test_should_return_an_error_when_the_api_key_is_not_configured():

    config = Config()
    onboarding = Onboarding.from_config(config)

    result = onboarding.create_user()

    assert_failure(result)


def test_should_do_complete_onboarding_process(
    given_valid_api_key,
    given_any_selfie_image_media_data,
    given_any_document_front_media_data,
    given_any_document_back_media_data,
    given_any_pdf_media_data,
):
    @meiga
    def do_complete_onboarding() -> Result[dict, Error]:
        config = Config(api_key=given_valid_api_key)

        onboarding = Onboarding.from_config(config)

        user_id = onboarding.create_user().unwrap_or_return()
        onboarding.add_selfie(
            user_id=user_id, media_data=given_any_selfie_image_media_data
        ).unwrap_or_return()
        document_id = onboarding.create_document(
            user_id=user_id, type="idcard", issuing_country="ESP"
        ).unwrap_or_return()
        onboarding.add_document(
            user_id=user_id,
            document_id=document_id,
            media_data=given_any_document_front_media_data,
            side="front",
            manual=True,
        ).unwrap_or_return()
        onboarding.add_document(
            user_id=user_id,
            document_id=document_id,
            media_data=given_any_document_back_media_data,
            side="back",
            manual=True,
        ).handle()
        onboarding.add_other_trusted_document(
            user_id=user_id, pdf=given_any_pdf_media_data
        ).unwrap_or_return()
        onboarding.document_properties(
            user_id=user_id, document_id=document_id
        ).unwrap_or_return()
        report = onboarding.create_report(user_id=user_id).unwrap_or_return()

        certificate_id = onboarding.create_certificate(
            user_id=user_id
        ).unwrap_or_return()

        _ = onboarding.retrieve_certificate(
            user_id=user_id, certificate_id=certificate_id
        ).unwrap_or_return()

        _ = onboarding.retrieve_certificates(user_id=user_id).unwrap_or_return()

        onboarding.delete_user(user_id).unwrap_or_return()

        return Success(report)

    result = do_complete_onboarding()

    assert_success(result, value_is_instance_of=Dict)
