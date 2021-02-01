import time
import json
import jwt
import requests
from requests import Response
from alice.onboarding.tools import timeit, print_intro, print_response


class AuthClient:
    def __init__(self, url, api_key):
        self.url = url
        self._api_key = api_key
        self._login_token = None

    @timeit
    def create_backend_token(
        self, user_id: str = None, verbose: bool = False
    ) -> Response:

        suffix = " (with user)" if user_id else ""
        print_intro(f"create_backend_token{suffix}", verbose=verbose)

        if not self._is_valid_token(self._login_token):
            response = self._create_login_token()
            if response.status_code == 200:
                self._login_token = self._get_token_from_response(response)
            else:
                return response

        final_url = f"{self.url}/backend_token"
        if user_id:
            final_url += f"/{user_id}"

        headers = {"Authorization": f"Bearer {self._login_token}"}
        response = requests.get(final_url, headers=headers)
        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def create_user_token(self, user_id: str, verbose: bool = False) -> Response:

        print_intro("create_user_token", verbose=verbose)

        if not self._is_valid_token(self._login_token):
            response = self._create_login_token()
            if response.status_code == 200:
                self._login_token = self._get_token_from_response(response)
            else:
                return response

        final_url = f"{self.url}/user_token/{user_id}"
        headers = {"Authorization": f"Bearer {self._login_token}"}
        response = requests.get(final_url, headers=headers)

        print_response(response=response, verbose=verbose)

        return response

    def _create_login_token(self):
        final_url = f"{self.url}/login_token"
        headers = {"apikey": self._api_key}
        response = requests.get(final_url, headers=headers)

        return response

    @staticmethod
    def _is_valid_token(token, margin_seconds: int = 60):
        if not token:
            return False
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return decoded_token["exp"] > time.time() - margin_seconds

    @staticmethod
    def _get_token_from_response(response):
        response_json = json.loads(response.content)
        token = response_json["token"]
        return token
