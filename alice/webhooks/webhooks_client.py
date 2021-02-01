import platform
import requests
from requests import Response

from alice.auth.auth import Auth
from alice.onboarding.tools import timeit, print_intro, print_response, print_token

import alice
from alice.webhooks.webhook import Webhook

DEFAULT_URL = "https://apis.alicebiometrics.com/onboarding"


class WebhooksClient:
    def __init__(self, auth: Auth, url: str = DEFAULT_URL, send_agent: bool = True):
        self.auth = auth
        self.url = url
        self.send_agent = send_agent

    def _auth_headers(self, token: str):
        auth_headers = {"Authorization": f"Bearer {token}"}
        if self.send_agent:
            auth_headers.update(
                {
                    "Alice-User-Agent": f"onboarding-python/{alice.__version__} ({platform.system()}; {platform.release()}) python {platform.python_version()}"
                }
            )
        return auth_headers

    @timeit
    def get_available_events(self, verbose: bool = False) -> Response:
        """

        Get public available events.

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("get_available_events", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap()
        print_token("backend_token_with_user", backend_token, verbose=verbose)
        headers = self._auth_headers(backend_token)
        response = requests.get(self.url + "/events", headers=headers)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def create_webhook(
        self, webhook: Webhook = None, verbose: bool = False
    ) -> Response:
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
            A Response object [requests library]
        """
        print_intro("create_webhook", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap()

        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        headers["Content-Type"] = "application/json"

        data = None
        if webhook:
            data = data if data is not None else {}
            data.update(webhook.to_dict())

        response = requests.post(self.url + "/webhook", headers=headers, json=data)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def update_webhook(self, webhook: Webhook, verbose: bool = False) -> Response:
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
            A Response object [requests library]
        """
        print_intro("update_webhook", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        headers["Content-Type"] = "application/json"

        data = None
        if webhook:
            data = data if data is not None else {}
            data.update(webhook.to_dict())

        response = requests.put(
            self.url + f"/webhook/{webhook.webhook_id}", headers=headers, json=data
        )

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def update_webhook_activation(
        self, webhook_id: str, active: bool, verbose: bool = False
    ) -> Response:
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
             A Response object [requests library]
        """
        print_intro("update_webhook_activation", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        headers["Content-Type"] = "application/json"

        response = requests.patch(
            self.url + f"/webhook/{webhook_id}",
            headers=headers,
            json={"active": active},
        )

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def ping_webhook(self, webhook_id: str, verbose: bool = False) -> Response:
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
            A Response object [requests library]
        """
        print_intro("ping_webhook", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        response = requests.post(
            self.url + f"/webhook/{webhook_id}/ping", headers=headers
        )

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def delete_webhook(self, webhook_id: str, verbose: bool = False) -> Response:
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
            A Response object [requests library]
        """
        print_intro("delete_webhook", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        response = requests.delete(self.url + f"/webhook/{webhook_id}", headers=headers)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def get_webhook(self, webhook_id: str, verbose: bool = False) -> Response:
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
            A Response object [requests library]
        """
        print_intro("get_webhook", verbose=verbose)

        user_token = self.auth.create_backend_token().unwrap()
        print_token("user_token", user_token, verbose=verbose)

        headers = self._auth_headers(user_token)

        response = requests.get(self.url + f"/webhook/{webhook_id}", headers=headers)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def get_webhooks(self, verbose: bool = False) -> Response:
        """

        Returns all configured webhooks

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("get_webhooks", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap()
        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        response = requests.get(self.url + "/webhooks", headers=headers)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def get_webhook_results(self, webhook_id: str, verbose: bool = False) -> Response:
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
            A Response object [requests library]
        """
        print_intro("get_webhook_results", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap()
        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        response = requests.get(
            self.url + f"/webhook/results/{webhook_id}", headers=headers
        )

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def get_last_webhook_result(
        self, webhook_id: str, verbose: bool = False
    ) -> Response:
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
            A Response object [requests library]
        """
        print_intro("get_last_webhook_result", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap()
        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        response = requests.get(
            self.url + f"/webhook/result/{webhook_id}/last", headers=headers
        )

        print_response(response=response, verbose=verbose)

        return response
