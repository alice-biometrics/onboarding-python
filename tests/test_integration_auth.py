import pytest

from alice import Auth, Config
from alice.auth.auth_errors import AuthError
from alice.onboarding.onboarding import Onboarding


@pytest.mark.unit
class TestAuth:
    user_id: str

    def setup_method(self):
        self.user_id = "85c38a91-e4f8-4d51-b3b5-2db7dc98ada0"

    def _get_user_id(self, config: Config) -> str:
        onboarding = Onboarding.from_config(config)
        return onboarding.create_user().unwrap_or_raise()

    def should_return_an_error_when_the_api_key_is_not_configured(self):
        config = Config()
        auth = Auth.from_config(config)

        result = auth.create_backend_token()
        result.assert_failure(value_is_instance_of=AuthError)

    def should_create_a_valid_backend_token(self, given_valid_api_key):

        config = Config(api_key=given_valid_api_key)
        auth = Auth.from_config(config)

        result = auth.create_backend_token()
        result.assert_success(value_is_instance_of=str)

    def should_create_a_valid_backend_token_with_timeout(self, given_valid_api_key):

        config = Config(api_key=given_valid_api_key, timeout=5)
        auth = Auth.from_config(config)

        result = auth.create_backend_token()
        result.assert_success(value_is_instance_of=str)

    def should_create_a_valid_backend_token_with_user(self, given_valid_api_key):

        config = Config(api_key=given_valid_api_key)
        auth = Auth.from_config(config)

        result = auth.create_backend_token(user_id=self._get_user_id(config))
        result.assert_success(value_is_instance_of=str)

    def should_create_a_valid_user_token(self, given_valid_api_key):

        config = Config(api_key=given_valid_api_key)
        auth = Auth.from_config(config)

        onboarding = Onboarding.from_config(config)
        user_id = onboarding.create_user().unwrap_or_raise()

        result = auth.create_user_token(user_id=self._get_user_id(config))
        result.assert_success(value_is_instance_of=str)
