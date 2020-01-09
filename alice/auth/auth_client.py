import time
import json
import jwt
import requests
from requests import Response


class AuthClient:
    def __init__(self, base_url, api_key):
        self._base_url = base_url
        self._api_key = api_key
        self._login_token = None

    def create_backend_token(self, service_id: str, user_id: str = None) -> Response:
        if not self._is_token_valid(self._login_token):
            response = self._create_login_token()
            if response.status_code == 200:
                self._login_token = self._get_token_from_response(response)
            else:
                return response

        final_url = "{}/backend_token/{}".format(self._base_url, service_id)
        if user_id:
            final_url += "/{}".format(user_id)

        headers = {"Authorization": "Bearer {}".format(self._login_token)}
        response = requests.get(final_url, headers=headers)

        return response

    def create_user_token(self, service_id: str, user_id: str) -> Response:
        if not self._is_token_valid(self._login_token):
            response = self._create_login_token()
            if response.status_code == 200:
                self._login_token = self._get_token_from_response(response)
            else:
                return response

        final_url = "{}/user_token/{}/{}".format(self._base_url, service_id, user_id)
        headers = {"Authorization": "Bearer {}".format(self._login_token)}
        response = requests.get(final_url, headers=headers)

        return response

    def _create_login_token(self):
        final_url = "{}/login_token".format(self._base_url)
        headers = {"apikey": self._api_key}
        response = requests.get(final_url, headers=headers)
        return response

    @staticmethod
    def _is_token_valid(token, margin_seconds: int = 60):
        if not token:
            return False

        decoded_token = jwt.decode(token, verify=False)
        return decoded_token["exp"] > time.time() - margin_seconds

    @staticmethod
    def _get_token_from_response(response):
        response_json = json.loads(response.content)
        token = response_json["token"]
        return token
