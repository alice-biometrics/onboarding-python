import json
from typing import Optional, Union

import requests
from meiga import Failure, Result, Success
from requests import Response, Session

from alice.config import Config

from .auth_client import AuthClient
from .auth_errors import AuthError

DEFAULT_URL = "https://apis.alicebiometrics.com/onboarding"


class Auth:
    @staticmethod
    def from_config(config: Config) -> "Auth":
        if config.session:
            session = config.session
        else:
            session = requests.Session()
        return Auth(
            api_key=config.api_key,  # type: ignore
            session=session,
            url=config.onboarding_url,
            verbose=config.verbose,
        )

    def __init__(
        self,
        api_key: str,
        session: Session,
        url: str = DEFAULT_URL,
        verbose: Optional[bool] = False,
    ):
        self._auth_client = AuthClient(url=url, api_key=api_key, session=session)
        self.url = url
        self.verbose = verbose

    def create_backend_token(
        self, user_id: Union[str, None] = None, verbose: Optional[bool] = False
    ) -> Result[str, AuthError]:
        """
        Returns a BACKEND_TOKEN or BACKEND_TOKEN_WITH_USER depending of user_id given parameter.
        Both BACKEND_TOKEN and BACKEND_TOKEN_WITH_USER are used to secure global requests.

        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed

        Returns
        -------
            A Result where if the operation is successful it returns BACKEND_TOKEN or BACKEND_TOKEN_WITH_USER.
            Otherwise, it returns an OnboardingError.
        """
        verbose = self.verbose or verbose
        response = self._auth_client.create_backend_token(user_id, verbose=verbose)

        if response.status_code == 200:
            return Success(self.__get_token_from_response(response))
        else:
            suffix = " (with user)" if user_id else ""
            return Failure(
                AuthError.from_response(
                    operation=f"create_backend_token{suffix}", response=response
                )
            )

    def create_user_token(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Result[str, AuthError]:
        """
        Returns a USER_TOKEN.
        The USER_TOKEN is used to secure requests made by the users on their mobile devices or web clients.


        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns USER_TOKEN.
            Otherwise, it returns an OnboardingError.
        """
        verbose = self.verbose or verbose
        response = self._auth_client.create_user_token(user_id, verbose=verbose)

        if response.status_code == 200:
            return Success(self.__get_token_from_response(response))
        else:
            return Failure(
                AuthError.from_response(
                    operation="create_user_token", response=response
                )
            )

    @staticmethod
    def __get_token_from_response(response: Response) -> str:
        response_json = json.loads(response.content)
        token: str = response_json["token"]
        return token
