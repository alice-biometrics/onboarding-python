import time
from typing import Dict

import jwt

from alice.config import Config
from alice.sandbox.sandbox_client import SandboxClient
from alice.sandbox.sandbox_errors import SandboxError
from alice.onboarding.user_info import UserInfo
from alice.onboarding.device_info import DeviceInfo
from meiga import Result, Failure, isSuccess, Success

DEFAULT_URL = "https://apis.alicebiometrics.com/onboarding/sandbox"


class Sandbox:
    @staticmethod
    def from_config(config: Config):
        return Sandbox(sandbox_token=config.sandbox_token, url=config.sandbox_url)

    def __init__(self, sandbox_token: str, url: str = DEFAULT_URL):
        self.sandbox_client = SandboxClient(sandbox_token=sandbox_token, url=url)
        self.url = url

    @staticmethod
    def _is_token_valid(token, margin_seconds: int = 60):
        if not token:
            return False

        decoded_token = jwt.decode(token, verify=False)
        return decoded_token["exp"] > time.time() - margin_seconds

    def healthcheck(self, verbose: bool = False) -> Result[bool, SandboxError]:
        """
        Runs a healthcheck on the service to see if there are any problems.

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an SandboxError.
        """
        response = self.sandbox_client.healthcheck(verbose=verbose)

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                SandboxError.from_response(operation="healthcheck", response=response)
            )

    def create_user(
        self,
        user_info: UserInfo = None,
        device_info: DeviceInfo = None,
        verbose: bool = False,
    ) -> Result[str, SandboxError]:
        """

        It creates a new User in the Sandbox service.

        Note that in this service, email is a required property
        Note this command will execute also Onboarding User Creation.

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
            A Result where if the operation is successful it returns a user_id.
            Otherwise, it returns an SandboxError.
        """
        response = self.sandbox_client.create_user(
            user_info=user_info, device_info=device_info, verbose=verbose
        )

        if response.status_code == 200:
            return Success(response.json())
        else:
            return Failure(
                SandboxError.from_response(operation="create_user", response=response)
            )

    def delete_user(
        self, email: str, verbose: bool = False
    ) -> Result[bool, SandboxError]:
        """

        Delete all the information of a Sandbox User. Including the link with Onboarding user.
        Note this command will execute also Onboarding User Deletion.

        Parameters
        ----------
        email
            User's email
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an SandboxError.
        """
        response = self.sandbox_client.delete_user(email=email, verbose=verbose)

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                SandboxError.from_response(operation="delete_user", response=response)
            )

    def get_user(self, email: str, verbose: bool = False) -> Result[Dict, SandboxError]:
        """

        Returns User Status of a Sandbox user

        Parameters
        ----------
        email
            User's email
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns a Dict with the status info.
            Otherwise, it returns an SandboxError.
        """
        response = self.sandbox_client.get_user(email=email, verbose=verbose)

        if response.status_code == 200:
            return Success(response.json())
        else:
            return Failure(
                SandboxError.from_response(operation="get_user", response=response)
            )

    def get_user_token(
        self, email: str, verbose: bool = False
    ) -> Result[str, SandboxError]:
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
            A Result where if the operation is successful it returns list of string with already created user_ids.
            Otherwise, it returns an SandboxError.
        """
        response = self.sandbox_client.get_user_token(email=email, verbose=verbose)

        if response.status_code == 200:
            return Success(response.json()["user_token"])
        else:
            return Failure(
                SandboxError.from_response(
                    operation="get_user_token", response=response
                )
            )
