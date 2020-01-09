from typing import Dict

from meiga import Result, Error
from meiga.assertions import assert_success, assert_failure
from meiga.decorators import meiga

from alice import Onboarding, Config


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
):
    @meiga
    def do_complete_onboarding() -> Result[dict, Error]:
        config = Config(api_key=given_valid_api_key)

        onboarding = Onboarding.from_config(config)

        user_id = onboarding.create_user().handle()
        onboarding.add_selfie(
            user_id=user_id, media_data=given_any_selfie_image_media_data
        ).handle()
        document_id = onboarding.create_document(
            user_id=user_id, type="idcard", issuing_country="ESP"
        ).handle()
        onboarding.add_document(
            user_id=user_id,
            document_id=document_id,
            media_data=given_any_document_front_media_data,
            side="front",
            manual=True,
        ).handle()
        onboarding.add_document(
            user_id=user_id,
            document_id=document_id,
            media_data=given_any_document_back_media_data,
            side="back",
            manual=True,
        ).handle()
        return onboarding.create_report(user_id=user_id)

    result = do_complete_onboarding()

    assert_success(result, value_is_instance_of=Dict)