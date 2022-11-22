import platform
from typing import Any, Dict, Optional, Union

from meiga import Result, Success, early_return
from requests import Response, Session

import alice
from alice.auth.auth import Auth
from alice.auth.auth_errors import AuthError
from alice.onboarding.tools import print_intro, print_response, print_token, timeit
from alice.webhooks.webhook import Webhook

DEFAULT_URL = "https://apis.alicebiometrics.com/onboarding"


class WebhooksClient:
    def __init__(
        self,
        auth: Auth,
        session: Session,
        url: str = DEFAULT_URL,
        send_agent: bool = True,
    ):
        self.auth = auth
        self.url = url
        self.send_agent = send_agent
        self.session = session

    def _auth_headers(self, token: str) -> Dict[str, Any]:
        auth_headers = {"Authorization": f"Bearer {token}"}
        if self.send_agent:
            auth_headers.update(
                {
                    "Alice-User-Agent": f"onboarding-python/{alice.__version__} ({platform.system()}; {platform.release()}) python {platform.python_version()}"
                }
            )
        return auth_headers

    @early_return
    @timeit
    def get_available_events(
        self, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
        """

        Get public available events.

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library] if success
        """
        print_intro("get_available_events", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap_or_return()
        print_token("backend_token_with_user", backend_token, verbose=verbose)
        headers = self._auth_headers(backend_token)
        response = self.session.get(self.url + "/events", headers=headers)

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def create_webhook(
        self, webhook: Union[Webhook, None] = None, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
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
            A Response object [requests library] if success
        """
        print_intro("create_webhook", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap_or_return()

        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        headers["Content-Type"] = "application/json"

        data = None
        if webhook:
            data = data if data is not None else {}
            data.update(webhook.to_dict())

        response = self.session.post(self.url + "/webhook", headers=headers, json=data)

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def update_webhook(
        self, webhook: Webhook, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
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
            A Response object [requests library] if success
        """
        print_intro("update_webhook", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap_or_return()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        headers["Content-Type"] = "application/json"

        data = None
        if webhook:
            data = data if data is not None else {}
            data.update(webhook.to_dict())

        response = self.session.put(
            self.url + f"/webhook/{webhook.webhook_id}", headers=headers, json=data
        )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def update_webhook_activation(
        self, webhook_id: str, active: bool, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
        """

        Update Webhook activation

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
            A Response object [requests library] if success
        """
        print_intro("update_webhook_activation", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap_or_return()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        headers["Content-Type"] = "application/json"

        response = self.session.patch(
            self.url + f"/webhook/{webhook_id}",
            headers=headers,
            json={"active": active},
        )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def ping_webhook(
        self, webhook_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
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
            A Response object [requests library] if success
        """
        print_intro("ping_webhook", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap_or_return()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        response = self.session.post(
            self.url + f"/webhook/{webhook_id}/ping", headers=headers
        )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def delete_webhook(
        self, webhook_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
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
            A Response object [requests library] if success
        """
        print_intro("delete_webhook", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap_or_return()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        response = self.session.delete(
            self.url + f"/webhook/{webhook_id}", headers=headers
        )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def get_webhook(
        self, webhook_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
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
            A Response object [requests library] if success
        """
        print_intro("get_webhook", verbose=verbose)

        user_token = self.auth.create_backend_token().unwrap_or_return()
        print_token("user_token", user_token, verbose=verbose)

        headers = self._auth_headers(user_token)

        response = self.session.get(
            self.url + f"/webhook/{webhook_id}", headers=headers
        )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def get_webhooks(
        self, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
        """

        Returns all configured webhooks

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library] if success
        """
        print_intro("get_webhooks", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap_or_return()
        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        response = self.session.get(self.url + "/webhooks", headers=headers)

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def get_webhook_results(
        self, webhook_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
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
            A Response object [requests library] if success
        """
        print_intro("get_webhook_results", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap_or_return()
        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        response = self.session.get(
            self.url + f"/webhook/results/{webhook_id}", headers=headers
        )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def get_last_webhook_result(
        self, webhook_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
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
            A Response object [requests library] if success
        """
        print_intro("get_last_webhook_result", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap_or_return()
        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        response = self.session.get(
            self.url + f"/webhook/result/{webhook_id}/last", headers=headers
        )

        print_response(response=response, verbose=verbose)

        return Success(response)
