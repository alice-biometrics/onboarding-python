from typing import Any, Dict, List, Optional, Union

from meiga import Failure, Result, Success, early_return, isSuccess
from requests import Session

from alice.auth.auth import Auth
from alice.auth.auth_errors import AuthError
from alice.config import Config
from alice.onboarding.onboarding_errors import OnboardingError
from alice.webhooks.webhook import Webhook
from alice.webhooks.webhooks_client import WebhooksClient

DEFAULT_URL = "https://apis.alicebiometrics.com/onboarding"


class Webhooks:
    @staticmethod
    def from_config(config: Config) -> "Webhooks":
        if config.session:
            session = config.session
        else:
            session = Session()
        return Webhooks(
            auth=Auth.from_config(config),
            url=config.onboarding_url,  # type: ignore
            send_agent=config.send_agent,
            verbose=config.verbose,
            session=session,
        )

    def __init__(
        self,
        auth: Auth,
        session: Session,
        url: str = DEFAULT_URL,
        send_agent: bool = True,
        verbose: Optional[bool] = False,
    ):
        self.webhooks_client = WebhooksClient(
            auth=auth, url=url, send_agent=send_agent, session=session
        )
        self.url = url
        self.verbose = verbose

    @early_return
    def get_subscriptable_events(
        self, verbose: Optional[bool] = False
    ) -> Result[bool, Union[OnboardingError, AuthError]]:
        """
        Get public subscriptable events.

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.webhooks_client.get_subscriptable_events(
            verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json())
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="get_subscriptable_events", response=response
                )
            )

    @early_return
    def create_webhook(
        self, webhook: Webhook, verbose: Optional[bool] = False
    ) -> Result[str, Union[OnboardingError, AuthError]]:
        """

        It creates a new Webhook in the onboarding service.

        Parameters
        ----------
        webhook
            Object with Webhook information.
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns a webhook_id.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.webhooks_client.create_webhook(
            webhook=webhook, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json()["webhook_id"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="create_webhook", response=response
                )
            )

    @early_return
    def update_webhook(
        self, webhook: Webhook, verbose: Optional[bool] = False
    ) -> Result[Dict[str, Any], Union[OnboardingError, AuthError]]:
        """

        Update an existent Webhook

        Parameters
        ----------
        webhook
            Object with Webhook information.
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns a webhook_id.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.webhooks_client.update_webhook(
            webhook=webhook, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="update_webhook", response=response
                )
            )

    @early_return
    def update_webhook_activation(
        self, webhook_id: str, active: bool, verbose: Optional[bool] = False
    ) -> Result[Dict[str, Any], Union[OnboardingError, AuthError]]:
        """

        Update the activation of a Webhook

        Parameters
        ----------
        webhook_id
            Webhook identifier
        active
            Activation boolean value
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns a webhook_id.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.webhooks_client.update_webhook_activation(
            webhook_id=webhook_id, active=active, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="update_webhook_activation", response=response
                )
            )

    @early_return
    def ping_webhook(
        self, webhook_id: str, verbose: Optional[bool] = False
    ) -> Result[bool, Union[OnboardingError, AuthError]]:
        """
        Send ping event to configured and active Webhook

        Parameters
        ----------
        webhook_id
            Webhook identifier
        verbose
            Used for print service response as well as the time elapsed

        Returns
        -------
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.webhooks_client.ping_webhook(
            webhook_id=webhook_id, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200 or response.status_code == 201:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="ping_webhook", response=response
                )
            )

    @early_return
    def delete_webhook(
        self, webhook_id: str, verbose: Optional[bool] = False
    ) -> Result[bool, Union[OnboardingError, AuthError]]:
        """
        Remove a configured Webhook

        Parameters
        ----------
        webhook_id
            Webhook identifier
        verbose
            Used for print service response as well as the time elapsed

        Returns
        -------
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.webhooks_client.delete_webhook(
            webhook_id=webhook_id, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="delete_webhook", response=response
                )
            )

    @early_return
    def get_webhook(
        self, webhook_id: str, verbose: Optional[bool] = False
    ) -> Result[Webhook, Union[OnboardingError, AuthError]]:
        """
        Returns Webhook info

        Parameters
        ----------
        webhook_id
            Webhook identifier
        verbose
            Used for print service response as well as the time elapsed

        Returns
        -------
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.webhooks_client.get_webhook(
            webhook_id=webhook_id, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(Webhook.from_dict(response.json()))
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="get_webhook", response=response
                )
            )

    @early_return
    def get_webhooks(
        self, verbose: Optional[bool] = False
    ) -> Result[List[Webhook], Union[OnboardingError, AuthError]]:
        """
        Returns Webhook info

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed

        Returns
        -------
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.webhooks_client.get_webhooks(verbose=verbose).unwrap_or_return()

        if response.status_code == 200:
            webhooks = response.json()
            webhooks = [Webhook.from_dict(webhook) for webhook in webhooks]
            return Success(webhooks)
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="get_webhooks", response=response
                )
            )

    @early_return
    def get_webhook_results(
        self, webhook_id: str, verbose: Optional[bool] = False
    ) -> Result[Webhook, Union[OnboardingError, AuthError]]:
        """
        Returns all the result of delivered events from a specific Webhook

        Parameters
        ----------
        webhook_id
            Webhook identifier
        verbose
            Used for print service response as well as the time elapsed

        Returns
        -------
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.webhooks_client.get_webhook_results(
            webhook_id=webhook_id, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json())
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="get_webhook_results", response=response
                )
            )

    @early_return
    def get_last_webhook_result(
        self, webhook_id: str, verbose: Optional[bool] = False
    ) -> Result[Webhook, Union[OnboardingError, AuthError]]:
        """
        Returns last result of delivered event from a specific Webhook

        Parameters
        ----------
        webhook_id
            Webhook identifier
        verbose
            Used for print service response as well as the time elapsed

        Returns
        -------
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.webhooks_client.get_last_webhook_result(
            webhook_id=webhook_id, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json())
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="get_last_webhook_result", response=response
                )
            )
