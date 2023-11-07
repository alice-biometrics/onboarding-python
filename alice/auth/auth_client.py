from typing import Optional, Union
from unittest.mock import Mock

import requests
from meiga import Failure, Result, Success
from requests import Response, Session

from alice.auth.cached_token_stack import CachedTokenStack
from alice.auth.token_tools import (
    get_reponse_from_token,
    get_token_from_response,
    is_valid_token,
)
from alice.onboarding.tools import print_intro, print_response, timeit


def get_response_timeout() -> Response:
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
        use_cache: bool = False,
    ):
        self.url = url
        self._api_key = api_key
        self._cached_login_token: Union[str, None] = None
        self._cached_backend_token: Union[str, None] = None
        self._cached_backend_token_stack = CachedTokenStack()
        self._cached_user_token_stack = CachedTokenStack()
        self.session = session
        self.timeout = timeout
        self.use_cache = use_cache

    @timeit
    def create_user_token(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Response:
        print_intro("create_user_token", verbose=verbose)

        token = self._cached_user_token_stack.get(user_id)
        if token:
            return get_reponse_from_token(token)

        result = self._get_login_token()
        if result.is_failure:
            return result.value  # type: ignore
        login_token = result.unwrap()

        url = f"{self.url}/user_token/{user_id}"
        headers = {"Authorization": f"Bearer {login_token}"}
        if self.use_cache:
            headers["Cache-Control"] = "use-cache"
        try:
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                self._cached_user_token_stack.add(
                    user_id, get_token_from_response(response)
                )
        except requests.exceptions.Timeout:
            response = get_response_timeout()

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def create_backend_token(
        self, user_id: Union[str, None] = None, verbose: Optional[bool] = False
    ) -> Response:
        if user_id:
            return self._create_backend_token_with_user_id(user_id, verbose)
        else:
            return self._create_backend_token(verbose)

    def _create_backend_token(self, verbose: Optional[bool] = False) -> Response:
        print_intro("create_backend_token", verbose=verbose)

        token = self._get_cached_backend_token()
        if token:
            return get_reponse_from_token(token)

        result = self._get_login_token()
        if result.is_failure:
            return result.value  # type: ignore
        login_token = result.unwrap()
        url = f"{self.url}/backend_token"
        headers = {"Authorization": f"Bearer {login_token}"}
        if self.use_cache:
            headers["Cache-Control"] = "use-cache"
        try:
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                self._cached_backend_token = get_token_from_response(response)
        except requests.exceptions.Timeout:
            response = get_response_timeout()

        print_response(response=response, verbose=verbose)

        return response

    def _get_cached_backend_token(self) -> Union[str, None]:
        if not is_valid_token(self._cached_backend_token):
            return None
        return self._cached_backend_token

    def _create_backend_token_with_user_id(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Response:
        print_intro("create_backend_token (with user)", verbose=verbose)

        token = self._cached_backend_token_stack.get(user_id)
        if token:
            return get_reponse_from_token(token)

        result = self._get_login_token()
        if result.is_failure:
            return result.value  # type: ignore
        login_token = result.unwrap()

        url = f"{self.url}/backend_token/{user_id}"
        headers = {"Authorization": f"Bearer {login_token}"}
        if self.use_cache:
            headers["Cache-Control"] = "use-cache"
        try:
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                self._cached_backend_token_stack.add(
                    user_id, get_token_from_response(response)
                )
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
        return Success(self._cached_login_token)  # type: ignore

    def _create_login_token(self) -> Response:
        final_url = f"{self.url}/login_token"
        headers = {"apikey": self._api_key}
        if self.use_cache:
            headers["Cache-Control"] = "use-cache"
        try:
            response = self.session.get(
                final_url, headers=headers, timeout=self.timeout
            )
        except requests.exceptions.Timeout:
            response = get_response_timeout()

        return response
