import json
import platform

from requests import request, Response

from alice.auth.auth import Auth
from alice.onboarding.tools import timeit, print_intro, print_response, print_token

from alice.onboarding.user_info import UserInfo
from alice.onboarding.device_info import DeviceInfo
import alice

DEFAULT_URL = "https://apis.alicebiometrics.com/auth"


class OnboardingClient:
    def __init__(self, auth: Auth, url: str = DEFAULT_URL, send_agent: bool = True):
        self.auth = auth
        self.url = url
        self.send_agent = send_agent

    def _auth_headers(self, token: str):
        auth_headers = {"Authorization": "Bearer {}".format(token)}
        if self.send_agent:
            auth_headers.update(
                {
                    "Alice-User-Agent": "onboarding-python/{} ({}; {}) python {}".format(
                        alice.__version__,
                        platform.system(),
                        platform.release(),
                        platform.python_version(),
                    )
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

        response = request("GET", self.url + "/healthcheck")

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

        response = request("POST", self.url + "/user", headers=headers, data=data)

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
        response = request("DELETE", self.url + "/user", headers=headers)

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

        response = request("GET", self.url + "/user/status", headers=headers)

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
        response = request("GET", self.url + "/users/stats", headers=headers)

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
        response = request("GET", self.url + "/users", headers=headers)

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

        response = request(
            "GET", self.url + "/users/status" + url_query_params, headers=headers
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

        response = request(
            "POST", self.url + "/user/selfie", files=files, headers=headers
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

        response = request("DELETE", self.url + "/user/selfie", headers=headers)

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

        response = request("PATCH", self.url + "/user/selfie", headers=headers)

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
        user_token = self.auth.create_user_token(user_id).unwrap()
        print_token("user_token", user_token, verbose=verbose)

        headers = self._auth_headers(user_token)

        response = request("GET", self.url + "/documents/supported", headers=headers)
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
            Type of document [idcard, driverlicense, passport]
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
        response = request(
            "POST", self.url + "/user/document", data=data, headers=headers
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
        response = request(
            "DELETE",
            self.url + "/user/document/{document_id}".format(document_id=document_id),
            headers=headers,
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
        response = request(
            "PATCH",
            self.url + "/user/document/{document_id}".format(document_id=document_id),
            headers=headers,
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

        files = {"image": ("image", media_data)}

        response = request(
            "PUT", self.url + "/user/document", files=files, data=data, headers=headers
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

        response = request(
            "POST", self.url + "/user/document/properties", data=data, headers=headers
        )

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def create_report(self, user_id: str, verbose: bool = False) -> Response:
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


        Returns
        -------
              A Response object [requests library]
        """
        print_intro("create_report", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(user_id=user_id).unwrap()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)
        response = request("GET", self.url + "/user/report", headers=headers)

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
        response = request("POST", self.url + "/user/authorize", headers=headers)

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
        response = request("POST", self.url + "/user/deauthorize", headers=headers)

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

        response = request(
            "POST", self.url + "/user/authenticate", files=files, headers=headers
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

        response = request(
            "GET", self.url + "/user/authentications/ids", headers=headers
        )

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

        response = request(
            "GET",
            self.url + "/user/authentications" + url_query_params,
            headers=headers,
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
        response = request(
            "GET",
            self.url
            + "/user/authentication/{authentication_id}".format(
                authentication_id=authentication_id
            ),
            headers=headers,
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

        response = request(
            "GET", self.url + "/media/{}/download".format(media_id), headers=headers
        )

        print_response(response=response, verbose=verbose)

        return response
