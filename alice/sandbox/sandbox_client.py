from typing import Any, Dict, Optional, Union

from requests import Response, request

from alice.onboarding.models.device_info import DeviceInfo
from alice.onboarding.models.user_info import UserInfo
from alice.onboarding.tools import print_intro, print_response, timeit

DEFAULT_URL = "https://apis.alicebiometrics.com/onboarding/sandbox"


class SandboxClient:
    def __init__(self, sandbox_token: str, url: str = DEFAULT_URL):
        self.sandbox_token = sandbox_token
        self.url = url

    def _auth_headers(self, token: str) -> Dict[str, Any]:
        auth_headers = {"Authorization": f"Bearer {token}"}
        return auth_headers

    @timeit
    def healthcheck(self, verbose: Optional[bool] = False) -> Response:
        """

        Runs a healthcheck on the service to see if there are any problems.

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("healthcheck", verbose=verbose)

        response = request("GET", self.url + "/healthcheck")

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def create_user(
        self,
        user_info: Union[UserInfo, None] = None,
        device_info: Union[DeviceInfo, None] = None,
        verbose: Optional[bool] = False,
    ) -> Response:
        """

        It creates a new User in the sandbox service.

        Parameters
        ----------
        user_info
            Object with optional values with info about the User.
        device_info
            Object with optional values with info about the User's Device.
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("create_user", verbose=verbose)

        headers = self._auth_headers(self.sandbox_token)

        data = None
        if user_info:
            data = data if data is not None else {}
            data.update(user_info.dict())
        if device_info:
            data = data if data is not None else {}
            data.update(device_info.dict())

        response = request("POST", self.url + "/user", headers=headers, data=data)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def delete_user(self, email: str, verbose: Optional[bool] = False) -> Response:
        """

        Delete all the information of a user

        Parameters
        ----------
        email
            User's email
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("delete_user", verbose=verbose)

        headers = self._auth_headers(self.sandbox_token)
        response = request("DELETE", self.url + f"/user/{email}", headers=headers)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def get_user(self, email: str, verbose: Optional[bool] = False) -> Response:
        """

        Returns User status to be used as feedback from the onboarding process

        Parameters
        ----------
        email
            User's email
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("get_user", verbose=verbose)

        headers = self._auth_headers(self.sandbox_token)

        response = request("GET", self.url + f"/user/{email}", headers=headers)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def get_user_token(self, email: str, verbose: Optional[bool] = False) -> Response:
        """

        Returns user token linked to Onboarding User managed by the Sandbox Service

        Parameters
        ----------
        email
            User's email
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("get_user_token", verbose=verbose)

        headers = self._auth_headers(self.sandbox_token)

        response = request("GET", self.url + f"/user/token/{email}", headers=headers)

        print_response(response=response, verbose=verbose)

        return response
