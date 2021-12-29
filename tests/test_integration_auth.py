import pytest
from meiga.assertions import assert_failure

from alice import Auth, Config


@pytest.mark.unit
def test_should_return_an_error_when_the_api_key_is_not_configured():

    config = Config()
    auth = Auth.from_config(config)

    result = auth.create_backend_token()

    assert_failure(result)


@pytest.mark.unit
def test_should_create_a_valid_backend_token(given_valid_api_key):

    config = Config(api_key=given_valid_api_key)
    auth = Auth.from_config(config)

    backend_token = auth.create_backend_token()

    assert backend_token is not None


@pytest.mark.unit
def test_should_create_a_valid_backend_token_with_user(given_valid_api_key):

    config = Config(api_key=given_valid_api_key)
    auth = Auth.from_config(config)

    backend_token_with_user = auth.create_backend_token(user_id="user_id")

    assert backend_token_with_user is not None


@pytest.mark.unit
def test_should_create_a_valid_user_token(given_valid_api_key):

    config = Config(api_key=given_valid_api_key)
    auth = Auth.from_config(config)

    user_token = auth.create_user_token(user_id="user_id")

    assert user_token is not None
