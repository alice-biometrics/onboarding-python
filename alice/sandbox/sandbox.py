import time
from typing import Any, Dict, Optional, Union

import jwt
from meiga import Failure, Result, Success, isSuccess

from alice.config import Config
from alice.onboarding.models.device_info import DeviceInfo
from alice.onboarding.models.user_info import UserInfo
from alice.sandbox.sandbox_client import SandboxClient
from alice.sandbox.sandbox_errors import SandboxError

DEFAULT_URL = "https://apis.alicebiometrics.com/onboarding/sandbox"


class Sandbox:
    @staticmethod
    def from_config(config: Config) -> "Sandbox":
        return Sandbox(
            sandbox_token=config.sandbox_token,  # type: ignore
            url=config.sandbox_url,
            verbose=config.verbose,
        )

    def __init__(
        self,
        sandbox_token: str,
        url: str = DEFAULT_URL,
        verbose: Optional[bool] = False,
    ) -> None:
        self.sandbox_client = SandboxClient(sandbox_token=sandbox_token, url=url)
        self.url = url
        self.verbose = verbose

    @staticmethod
    def _is_token_valid(token: Union[str, None], margin_seconds: int = 60) -> bool:
        if not token:
            return False

        decoded_token = jwt.decode(token, verify=False)
        return bool(decoded_token["exp"] > time.time() - margin_seconds)

    def healthcheck(
        self, verbose: Optional[bool] = False
    ) -> Result[bool, SandboxError]:
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
        verbose = self.verbose or verbose
        response = self.sandbox_client.healthcheck(verbose=verbose)

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                SandboxError.from_response(operation="healthcheck", response=response)
            )

    def create_user(
        self,
        user_info: Union[UserInfo, None] = None,
        device_info: Union[DeviceInfo, None] = None,
        verbose: Optional[bool] = False,
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
        verbose = self.verbose or verbose
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
        self, email: str, verbose: Optional[bool] = False
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
        verbose = self.verbose or verbose
        response = self.sandbox_client.delete_user(email=email, verbose=verbose)

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                SandboxError.from_response(operation="delete_user", response=response)
            )

    def get_user(
        self, email: str, verbose: Optional[bool] = False
    ) -> Result[Dict[str, Any], SandboxError]:
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
        verbose = self.verbose or verbose
        response = self.sandbox_client.get_user(email=email, verbose=verbose)

        if response.status_code == 200:
            return Success(response.json())
        else:
            return Failure(
                SandboxError.from_response(operation="get_user", response=response)
            )

    def get_user_token(
        self, email: str, verbose: Optional[bool] = False
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
        verbose = self.verbose or verbose
        response = self.sandbox_client.get_user_token(email=email, verbose=verbose)

        if response.status_code == 200:
            return Success(response.json()["user_token"])
        else:
            return Failure(
                SandboxError.from_response(
                    operation="get_user_token", response=response
                )
            )
