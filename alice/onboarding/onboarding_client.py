import json
import platform

import requests
from requests import Response
from typing import List

from alice.auth.auth import Auth
from alice.onboarding.decision import Decision
from alice.onboarding.document_source import DocumentSource
from alice.onboarding.report_version import ReportVersion
from alice.onboarding.tools import timeit, print_intro, print_response, print_token

from alice.onboarding.device_info import DeviceInfo
import alice
from alice.onboarding.user_info import UserInfo

DEFAULT_URL = "https://apis.alicebiometrics.com/onboarding"


class OnboardingClient:
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
    def healthcheck(self, verbose: bool = False) -> Response:
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

        response = requests.get(f"{self.url}/healthcheck")

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def create_user(
        self,
        user_info: UserInfo = None,
        device_info: DeviceInfo = None,
        verbose: bool = False,
    ) -> Response:
        """

        It creates a new User in the onboarding service.
        You must create a User before you start the onboarding flow.


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

        backend_token = self.auth.create_backend_token().unwrap()

        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)

        data = None
        if user_info:
            data = data if data is not None else {}
            data.update(json.loads(user_info.to_json()))
        if device_info:
            data = data if data is not None else {}
            data.update(json.loads(device_info.to_json()))

        response = requests.post(f"{self.url}/user", headers=headers, data=data)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def delete_user(self, user_id: str, verbose: bool = False) -> Response:
        """

        Delete all the information of a user

        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("delete_user", verbose=verbose)

        backend_token = self.auth.create_backend_token(user_id).unwrap()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        response = requests.delete(f"{self.url}/user", headers=headers)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def get_user_status(self, user_id: str, verbose: bool = False) -> Response:
        """

        Returns User status to be used as feedback from the onboarding process

        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("get_user_status", verbose=verbose)

        user_token = self.auth.create_user_token(user_id).unwrap()
        print_token("user_token", user_token, verbose=verbose)

        headers = self._auth_headers(user_token)

        response = requests.get(f"{self.url}/user/status", headers=headers)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def get_users_stats(self, verbose: bool = False) -> Response:
        """

        Returns statistics about users in the Onboarding platform.

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("get_users_stats", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap()
        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        response = requests.get(f"{self.url}/users/stats", headers=headers)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def get_users(self, verbose: bool = False) -> Response:
        """

        Returns all users you have created, sorted by creation date in descending order.

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("get_users", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap()
        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        response = requests.get(f"{self.url}/users", headers=headers)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def get_users_status(
        self,
        verbose: bool = False,
        page: int = 1,
        page_size: int = 0,
        descending: bool = True,
        authorized: bool = False,
        sort_by: str = None,
        filter_field: str = None,
        filter_value: str = None,
    ) -> Response:
        """

        Returns every UserStatus available for all the Users in the onboarding platform ordered by creation date.

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed.
        page
            Page from which users will be returned. Default 1.
        page_size
            Numbers of users that will be returned for each page. To return all the users select 0.
        descending
            Order of the users according to their creation date.
        authorized
            Only return authorized users.
        sort_by
            Field used for sorting the users.
        filter_field
            Field used for filtering the users.
        filter_value
            Value used for filtering the users.

        Returns
        -------
            A Response object [requests library]
        """
        print_intro("get_users_status", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap()
        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        url_query_params = f"?page={page}&page_size={page_size}&descending={descending}&authorized={authorized}"

        if filter_field and filter_value:
            url_query_params = (
                url_query_params
                + f"&filter_field={filter_field}&filter_value={filter_value}"
            )
        if sort_by:
            url_query_params = url_query_params + f"&sort_by={sort_by}"

        response = requests.get(
            f"{self.url}/users/status{url_query_params}", headers=headers
        )

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def add_user_feedback(
        self,
        user_id: str,
        document_id: str,
        selfie_media_id: str,
        decision: Decision,
        additional_feedback: List[str] = [],
        verbose: bool = False,
    ) -> Response:
        """

        Adds client's feedback about an user onboarding. Usually it comes after human review.

        Parameters
        ----------
        user_id
            User identifier
        document_id
            Document identifier
        selfie_media_id
            Selfie media identifier
        decision
            Whether user is accepted or rejected ["OK", "KO-client", "KO-alice"]
        additional_feedback
            List of strings containing additional feedback from user onboarding
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("add_user_feedback", verbose=verbose)

        backend_token = self.auth.create_backend_token(user_id).unwrap()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)

        data = {
            "document_id": document_id,
            "selfie_media_id": selfie_media_id,
            "decision": decision.value,
            "additional_feedback": additional_feedback,
        }

        response = requests.post(
            self.url + "/user/feedback", data=data, headers=headers
        )

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def add_selfie(
        self, user_id: str, media_data: bytes, verbose: bool = False
    ) -> Response:
        """

        This call is used to upload for the first time the video of the user's face to the onboarding service.
        This video will be used to extract the biometric face profile.

        Parameters
        ----------
        user_id
            User identifier
        media_data
            Binary media data.
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("add_selfie", verbose=verbose)

        user_token = self.auth.create_user_token(user_id).unwrap()
        print_token("user_token", user_token, verbose=verbose)

        headers = self._auth_headers(user_token)

        files = {"video": ("video", media_data)}

        response = requests.post(
            f"{self.url}/user/selfie", files=files, headers=headers
        )

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def delete_selfie(self, user_id: str, verbose: bool = False) -> Response:
        """

        This call is used to delete the video of the user's face to the onboarding service.
        This will also erase the biometric face profile.

        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("delete_selfie", verbose=verbose)

        backend_token = self.auth.create_backend_token(user_id).unwrap()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)

        response = requests.delete(f"{self.url}/user/selfie", headers=headers)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def void_selfie(self, user_id: str, verbose: bool = False) -> Response:
        """

        This call is used to void the video of the user's face to the onboarding service.
        This will NOT erase the biometric face profile.

        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("void_selfie", verbose=verbose)

        backend_token = self.auth.create_backend_token(user_id).unwrap()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)

        response = requests.patch(f"{self.url}/user/selfie", headers=headers)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def supported_documents(self, user_id: str, verbose: bool = False) -> Response:
        """
        This method is used to obtain a hierarchical-ordered dict with the information of the documents supported by the API.

        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("supported_documents", verbose=verbose)

        if user_id:
            token = self.auth.create_user_token(user_id).unwrap()
            print_token("user_token", token, verbose=verbose)
        else:
            token = self.auth.create_backend_token().unwrap()
            print_token("backend_token", token, verbose=verbose)

        headers = self._auth_headers(token)

        response = requests.get(f"{self.url}/documents/supported", headers=headers)
        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def create_document(
        self, user_id: str, type: str, issuing_country: str, verbose: bool = False
    ) -> Response:
        """

        This call is used to obtain a new document_id
        With this document_id you will be able to extract information with the add_document method

        Parameters
        ----------
        user_id
            User identifier
        type
            Type of document [idcard, driverlicense, passport, residencepermit, healthinsurancecard]
        issuing_country
            Issuing Country
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("create_document", verbose=verbose)
        user_token = self.auth.create_user_token(user_id).unwrap()
        print_token("user_token", user_token, verbose=verbose)

        headers = self._auth_headers(user_token)

        data = {"type": type, "issuing_country": issuing_country}
        response = requests.post(
            f"{self.url}/user/document", data=data, headers=headers
        )

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def delete_document(
        self, user_id: str, document_id: str, verbose: bool = False
    ) -> Response:
        """

        Delete all the stored/extracted information from a document


        Parameters
        ----------
        user_id
            User identifier
        document_id
            Document identifier
        verbose
            Used for print service response as well as the time elapsed

        Returns
        -------
            A Response object [requests library]
        """
        print_intro("delete_document", verbose=verbose)

        backend_token = self.auth.create_backend_token(user_id).unwrap()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        response = requests.delete(
            f"{self.url}/user/document/{document_id}", headers=headers
        )

        print_response(response=response, verbose=verbose)

        return response

    def void_document(
        self, user_id: str, document_id: str, verbose: bool = False
    ) -> Response:
        """

        Mark a document as invalid.


        Parameters
        ----------
        user_id
            User identifier
        document_id
            Document identifier
        verbose
            Used for print service response as well as the time elapsed

        Returns
        -------
            A Response object [requests library]
        """
        print_intro("void_document", verbose=verbose)

        backend_token = self.auth.create_backend_token(user_id).unwrap()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        response = requests.patch(
            f"{self.url}/user/document/{document_id}", headers=headers
        )

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def add_document(
        self,
        user_id: str,
        document_id: str,
        media_data: bytes,
        side: str,
        manual: bool = False,
        source: DocumentSource = DocumentSource.file,
        fields: dict = None,
        verbose: bool = False,
    ) -> Response:
        """

        This call is used to upload for the first time the photo or video of a document to the onboarding service.
        From a given media, the platform automatically saves the document content.

        Parameters
        ----------
        user_id
            User identifier
        document_id
            Document identifier
        media_data
            Binary media data.
        side
            Side of the document [front or back]
        manual
            If True defines manual document uploading
        source
            Source of the media: camera or file
        fields
            Fields to add regardless of the OCR process
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("add_document", verbose=verbose)

        user_token = self.auth.create_user_token(user_id).unwrap()
        print_token("user_token", user_token, verbose=verbose)

        headers = self._auth_headers(user_token)
        data = {
            "document_id": document_id,
            "side": side,
            "manual": manual,
            "fields": json.dumps(fields),
        }

        if source:
            data["source"] = source.value

        files = {"image": ("image", media_data)}

        response = requests.put(
            f"{self.url}/user/document", files=files, data=data, headers=headers
        )

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def document_properties(
        self, user_id: str, document_id: str, verbose: bool = False
    ) -> Response:
        """

        Returns the properties of a previously added document, such as face, MRZ or NFC availability


        Parameters
        ----------
        user_id
            User identifier
        document_id
            Document identifier
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("document_properties", verbose=verbose)

        user_token = self.auth.create_user_token(user_id).unwrap()
        print_token("user_token", user_token, verbose=verbose)

        headers = self._auth_headers(user_token)
        data = {"document_id": document_id}

        response = requests.post(
            f"{self.url}/user/document/properties", data=data, headers=headers
        )

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def create_report(
        self,
        user_id: str,
        verbose: bool = False,
        report_version: ReportVersion = ReportVersion.DEFAULT,
    ) -> Response:
        """

        This call is used to get the report of the onboarding process for a specific user.
        It returns information on all evidence that has been added and analyzed for that user,
        including documents and facial verifications.


        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed
        report_version
            Set Report Version

        Returns
        -------
              A Response object [requests library]
        """
        print_intro("create_report", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(user_id=user_id).unwrap()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)
        headers["Alice-Report-Version"] = report_version.value

        response = requests.get(f"{self.url}/user/report", headers=headers)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def create_certificate(
        self, user_id: str, template_name: str = "default", verbose: bool = False
    ) -> Response:
        """
        This call is used to create a Certificate (Signed PDF Report) of the onboarding process for a specific user.
        It returns a identifier (certificate_id) as a reference of created resource.
        This resource contains all evidence defined in the template.


        Parameters
        ----------
        user_id
            User identifier
        template_name
            'default' (only available)
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
              A Response object [requests library]
        """
        print_intro("create_certificate", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(user_id=user_id).unwrap()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)
        options = {"template_name": template_name}
        headers = self._auth_headers(backend_user_token)
        headers["Content-Type"] = "application/json"
        response = requests.post(
            f"{self.url}/user/certificate", data=json.dumps(options), headers=headers
        )

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def retrieve_certificate(
        self, user_id: str, certificate_id: str, verbose: bool = False
    ) -> Response:
        """

        This call is used to retrieve a Certificate (Signed PDF Report) of the onboarding process for a specific user.
        This resource contains all evidence defined in the template.


        Parameters
        ----------
        user_id
            User identifier
        certificate_id
            Certificate Unique Identifier
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
              A Response object [requests library]
        """
        print_intro("retrieve_certificate", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(user_id=user_id).unwrap()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)
        headers = self._auth_headers(backend_user_token)
        response = requests.get(
            f"{self.url}/user/certificate/{certificate_id}", headers=headers
        )

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def retrieve_certificates(self, user_id: str, verbose: bool = False) -> Response:
        """

        Returns summary info for created certificates

        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed

        Returns
        -------
              A Response object [requests library]
        """
        print_intro("retrieve_certificates", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(user_id=user_id).unwrap()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)
        headers = self._auth_headers(backend_user_token)
        response = requests.get(f"{self.url}/user/certificates", headers=headers)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def screening(
        self, user_id: str, detail: bool = False, verbose: bool = False
    ) -> Response:
        """
        This call is used to check on the user using different databases & lists (sanctions, PEP, etc)..
        It returns retrieved information from public lists.

        Parameters
        ----------
        user_id
            User identifier
        detail
            Used to select whether or not returns a summary detail
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
              A Response object [requests library]
        """
        print_intro("screening", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(user_id=user_id).unwrap()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)
        headers = self._auth_headers(backend_user_token)

        url = f"{self.url}/user/screening/search"
        if detail:
            url += "/detail"

        response = requests.get(url, headers=headers)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def screening_monitor_add(self, user_id: str, verbose: bool = False) -> Response:
        """
        This call is adds a user to the AML monitoring list.


        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
              A Response object [requests library]
        """
        print_intro("screening_monitor_add", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(user_id=user_id).unwrap()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)
        headers = self._auth_headers(backend_user_token)

        response = requests.get(f"{self.url}/user/screening/monitor", headers=headers)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def screening_monitor_delete(self, user_id: str, verbose: bool = False) -> Response:
        """
        This call is adds a user to the AML monitoring list.


        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
              A Response object [requests library]
        """
        print_intro("screening_monitor_delete", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(user_id=user_id).unwrap()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)
        headers = self._auth_headers(backend_user_token)

        response = requests.delete(
            f"{self.url}/user/screening/monitor", headers=headers
        )

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def screening_monitor_open_alerts(
        self, start_index: int = 0, size: int = 100, verbose: bool = False
    ) -> Response:
        """
        Retrieves from the monitoring list the users with open alerts

        Parameters
        ----------
        start_index
            DB index to start (0-2147483647)
        size
            Numbers of alerts to return (1-100).
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
              A Response object [requests library]
        """
        print_intro("screening_monitor_open_alerts", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap()
        print_token("backend_token", backend_token, verbose=verbose)
        headers = self._auth_headers(backend_token)

        response = requests.get(
            f"{self.url}/users/screening/monitor/alerts?start_index={start_index}&size={size}",
            headers=headers,
        )

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def identify_user(
        self, target_user_id: str, probe_user_ids: List[str], verbose: bool = False
    ) -> Response:
        """
        Identifies (1:N matching) a user against a N-length list of users.

        Parameters
        ----------
         target_user_id
            User identifier (Target)
        probe_user_ids
            List of user identifier to match against (N Probes)
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("identify_user", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(
            user_id=target_user_id
        ).unwrap()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)
        data = {"user_ids": probe_user_ids}

        response = requests.post(
            f"{self.url}/user/identify", headers=headers, data=data
        )

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def authorize_user(self, user_id: str, verbose: bool = False) -> Response:
        """
        Authorizes a user. Now it can be authenticate.

        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("authorize_user", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(user_id=user_id).unwrap()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)
        response = requests.post(f"{self.url}/user/authorize", headers=headers)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def deauthorize_user(self, user_id: str, verbose: bool = False) -> Response:
        """
        Deauthorizes a user. Now it cannot be authenticate.

        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("deauthorize_user", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(user_id=user_id).unwrap()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)
        response = requests.post(f"{self.url}/user/deauthorize", headers=headers)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def authenticate_user(
        self, user_id: str, media_data: bytes, verbose: bool = False
    ) -> Response:
        """

        Authenticates a previously registered User against a given media to verify the identity

        Parameters
        ----------
        user_id
            User identifier
        media_data
            Binary media data.
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("authenticate_user", verbose=verbose)

        user_token = self.auth.create_user_token(user_id=user_id).unwrap()
        print_token("user_token", user_token, verbose=verbose)

        headers = self._auth_headers(user_token)

        files = {"video": ("video", media_data)}

        response = requests.post(
            f"{self.url}/user/authenticate", files=files, headers=headers
        )

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def get_authentications_ids(self, user_id: str, verbose: bool = False) -> Response:
        """

        Returns all authentication you have performed for a User, sorted by creation date in descending order.

        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("get_authentications_ids", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(user_id=user_id).unwrap()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)

        response = requests.get(f"{self.url}/user/authentications/ids", headers=headers)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def get_authentications(
        self,
        user_id: str,
        page: int = 1,
        page_size: int = 0,
        descending: bool = True,
        verbose: bool = False,
    ) -> Response:
        """

        Returns all authentications you have performed for a User.

        Parameters
        ----------
        user_id
            User identifier
        page
            Page from which authentications will be returned. Default 1.
        page_size
            Numbers of authentications that will be returned for each page. To return all the authentications select 0.
        descending
            Order of the authentications according to their creation date.
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("get_authentications", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(user_id=user_id).unwrap()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)

        url_query_params = (
            f"?page={str(page)}&page_size={str(page_size)}&descending={str(descending)}"
        )

        response = requests.get(
            f"{self.url}/user/authentications" + url_query_params, headers=headers
        )

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def get_authentication(
        self, user_id: str, authentication_id: str, verbose: bool = False
    ) -> Response:
        """

        Gets a information from a previous authentication using the verification_id

        Parameters
        ----------
        user_id
            User identifier
        authentication_id
            Authentication identifier.
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("get_authentication", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(user_id=user_id).unwrap()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)
        response = requests.get(
            f"{self.url}/user/authentication/{authentication_id}", headers=headers
        )

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def retrieve_media(
        self, user_id: str, media_id: str, verbose: bool = False
    ) -> Response:
        """

        Returns the binary data of a media resource

        Parameters
        ----------
        user_id
            User identifier
        media_id
            Identifier obtained, for example from the report
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("retrieve_media", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(user_id=user_id).unwrap()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)

        response = requests.get(
            f"{self.url}/media/{media_id}/download", headers=headers
        )

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def download(self, user_id: str, href: str, verbose: bool = False) -> Response:
        """

        Returns the binary data of a media resource

        Parameters
        ----------
        user_id
            User identifier
        href
            href obtained, for example from the report
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("download", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(user_id=user_id).unwrap()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)

        response = requests.get(href, headers=headers)

        print_response(response=response, verbose=verbose)

        return response
