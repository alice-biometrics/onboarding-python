import json
from .auth_client import AuthClient

DEFAULT_URL = "https://apis.alicebiometrics.com/auth"


class AuthSdk:
    def __init__(
        self, api_key, service_id: str = "onboarding", base_url: str = DEFAULT_URL
    ):
        self._auth_client = AuthClient(base_url, api_key)
        self._service_id = service_id

    def create_backend_token(self, user_id: str = None) -> str:
        response = self._auth_client.create_backend_token(self._service_id, user_id)
        if response.status_code != 200:
            return None

        token = self.__get_token_from_response(response)
        return token

    def create_user_token(self, user_id: str) -> str:
        response = self._auth_client.create_user_token(self._service_id, user_id)

        if response.status_code != 200:
            return None

        token = self.__get_token_from_response(response)
        return token

    def check_user_token(self, user_token: str) -> str:
        response = self._auth_client.check_user_token(user_token)

        if response.status_code != 200:
            return None

        user_id = json.loads(response.content)
        return user_id

    @staticmethod
    def __get_token_from_response(response):
        response_json = json.loads(response.content)
        token = response_json["token"]
        return token
