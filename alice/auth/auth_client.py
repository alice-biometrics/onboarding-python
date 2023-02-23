from typing import Dict, Optional, Union
from unittest.mock import Mock

import requests
from meiga import Failure, Result, Success
from requests import Response, Session

from alice.auth.token_tools import get_token_from_response, is_valid_token
from alice.onboarding.tools import print_intro, print_response, timeit


def get_response_timeout():
    response = Mock(spec=Response)
    response.json.return_value = {"message": "Request timed out"}
    response.text.return_value = "Request timed out"
    response.status_code = 408
    return response


class AuthClient:
    def __init__(
        self,
        url: str,
        api_key: str,
        session: Session,
        timeout: Union[float, None] = None,
    ):
        self.url = url
        self._api_key = api_key
        self._cached_login_token: Union[str, None] = None
        self._cached_backend_token: Union[str, None] = None
        self._cached_backend_with_user_tokens: Union[Dict[str, str], None] = None
        self.session = session
        self.timeout = timeout

    @timeit
    def create_backend_token(
        self, user_id: Union[str, None] = None, verbose: Optional[bool] = False
    ) -> Response:
        if user_id:
            return self._create_backend_token_with_user_id(user_id, verbose)
        else:
            return self._create_backend_token(verbose)

    @timeit
    def create_user_token(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Response:

        print_intro("create_user_token", verbose=verbose)

        result = self._get_login_token()
        if result.is_failure:
            return result.value
        login_token = result.unwrap()

        url = f"{self.url}/user_token/{user_id}"
        headers = {"Authorization": f"Bearer {login_token}"}
        try:
            response = self.session.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            response = get_response_timeout()

        print_response(response=response, verbose=verbose)

        return response

    def _create_backend_token(self, verbose: Optional[bool] = False) -> Response:
        print_intro("create_backend_token", verbose=verbose)

        cached_backend_token = self._get_cached_backend_token()
        if cached_backend_token:
            return cached_backend_token

        result = self._get_login_token()
        if result.is_failure:
            return result.value
        login_token = result.unwrap()

        url = f"{self.url}/backend_token"
        headers = {"Authorization": f"Bearer {login_token}"}
        try:
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                self._cached_backend_token = response.json().get("token")
        except requests.exceptions.Timeout:
            response = get_response_timeout()

        print_response(response=response, verbose=verbose)

        return response

    def _get_cached_backend_token(self) -> Union[Response, None]:
        if not is_valid_token(self._cached_backend_token):
            return None

        response = Mock(spec=Response)
        response.json.return_value = {"token": self._cached_backend_token}
        response.status_code = 200
        return response

    def _create_backend_token_with_user_id(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Response:
        print_intro("create_backend_token (with user)", verbose=verbose)
        result = self._get_login_token()
        if result.is_failure:
            return result.value
        login_token = result.unwrap()

        url = f"{self.url}/backend_token/{user_id}"
        headers = {"Authorization": f"Bearer {login_token}"}
        try:
            response = self.session.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            response = get_response_timeout()

        print_response(response=response, verbose=verbose)

        return response

    def _get_login_token(self) -> Result[str, Response]:
        if not is_valid_token(self._cached_login_token):
            response = self._create_login_token()
            if response.status_code == 200:
                self._cached_login_token = get_token_from_response(response)
                return Success(self._cached_login_token)
            else:
                return Failure(response)
        return Success(self._cached_login_token)

    def _create_login_token(self) -> Response:
        final_url = f"{self.url}/login_token"
        headers = {"apikey": self._api_key}
        try:
            response = self.session.get(
                final_url, headers=headers, timeout=self.timeout
            )
        except requests.exceptions.Timeout:
            response = get_response_timeout()

        return response
