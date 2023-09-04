import pytest
from meiga.assertions import assert_failure, assert_success

from alice import Config, DeviceInfo, Sandbox, UserInfo


@pytest.mark.unit
def test_should_return_an_error_when_the_trial_token_is_not_configured():

    config = Config()
    sandbox = Sandbox.from_config(config)

    result = sandbox.create_user()

    assert_failure(result)


@pytest.mark.unit
def test_should_create_a_user_and_get_user_token_and_delete_it(
    given_valid_trial_token, given_any_valid_mail
):

    config = Config(trial_token=given_valid_trial_token)
    sandbox = Sandbox.from_config(config)

    result_create_user = sandbox.create_user(
        user_info=UserInfo(email=given_any_valid_mail),
        device_info=DeviceInfo(device_platform="Android"),
    )
    assert_success(result_create_user)

    result_user_token = sandbox.get_user_token(email=given_any_valid_mail)
    assert_success(result_user_token)

    result_delete_user = sandbox.delete_user(email=given_any_valid_mail)
    assert_success(result_delete_user)
