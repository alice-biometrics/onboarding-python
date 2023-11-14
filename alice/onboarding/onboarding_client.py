import json
import platform
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Union

import requests
from meiga import Error, Failure, Result, Success, early_return
from requests import Response, Session

import alice
from alice.auth.auth import Auth
from alice.onboarding.enums.certificate_locale import CertificateLocale
from alice.onboarding.enums.decision import Decision
from alice.onboarding.enums.document_side import DocumentSide
from alice.onboarding.enums.document_source import DocumentSource
from alice.onboarding.enums.document_type import DocumentType
from alice.onboarding.enums.duplicates_resource_type import DuplicatesResourceType
from alice.onboarding.enums.onboarding_steps import OnboardingSteps
from alice.onboarding.enums.user_state import UserState
from alice.onboarding.enums.version import Version
from alice.onboarding.models.bounding_box import BoundingBox
from alice.onboarding.models.device_info import DeviceInfo
from alice.onboarding.models.request_runner import RequestRunner
from alice.onboarding.models.user_info import UserInfo
from alice.onboarding.onboarding_errors import OnboardingError
from alice.onboarding.tools import print_intro, print_response, print_token, timeit

DEFAULT_URL = "https://apis.alicebiometrics.com/onboarding"


class OnboardingClient:
    def __init__(
        self,
        auth: Auth,
        session: Session,
        url: str = DEFAULT_URL,
        timeout: Union[float, None] = None,
        send_agent: bool = True,
    ):
        self.auth = auth
        self.url = url
        self.timeout = timeout
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

    @timeit
    def healthcheck(self, verbose: Optional[bool] = False) -> Result[Response, Error]:
        """

        Runs a healthcheck on the service to see if there are any problems.

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result object with Response object [requests library] if Success
        """
        print_intro("healthcheck", verbose=verbose)

        try:
            response = self.session.get(f"{self.url}/healthcheck", timeout=self.timeout)
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="healthcheck"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def create_user(
        self,
        user_info: Union[UserInfo, None] = None,
        device_info: Union[DeviceInfo, None] = None,
        flow_id: Union[str, None] = None,
        verbose: Optional[bool] = False,
    ) -> Result[Response, Error]:
        """

        It creates a new User in the onboarding service.
        You must create a User before you start the onboarding flow.


        Parameters
        ----------
        user_info
            Object with optional values with info about the User.
        device_info
            Object with optional values with info about the User's Device.
        flow_id
            Optional identifier of the onboarding flow
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result object with Response object [requests library] if Success
        """
        print_intro("create_user", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap_or_return()

        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)

        data = None
        if user_info:
            data = data if data is not None else {}
            data.update(user_info.dict())
        if device_info:
            data = data if data is not None else {}
            data.update(device_info.dict())
        if flow_id:
            data = data if data is not None else {}
            data.update({"flow_id": flow_id})
        try:
            response = self.session.post(
                f"{self.url}/user", headers=headers, data=data, timeout=self.timeout
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="create_user"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def delete_user(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, Error]:
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
            A Result object with Response object [requests library] if Success
        """
        print_intro("delete_user", verbose=verbose)

        backend_token = self.auth.create_backend_token(user_id).unwrap_or_return()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)

        try:
            response = self.session.delete(
                f"{self.url}/user", headers=headers, timeout=self.timeout
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="delete_user"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def get_user_status(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, Error]:
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
            A Result object with Response object [requests library] if Success
        """
        print_intro("get_user_status", verbose=verbose)

        user_token = self.auth.create_user_token(user_id).unwrap_or_return()
        print_token("user_token", user_token, verbose=verbose)

        headers = self._auth_headers(user_token)

        try:
            response = self.session.get(
                f"{self.url}/user/status", headers=headers, timeout=self.timeout
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="get_user_status"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def get_users_stats(
        self, verbose: Optional[bool] = False
    ) -> Result[Response, Error]:
        """

        Returns statistics about users in the Onboarding platform.

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result object with Response object [requests library] if Success
        """
        print_intro("get_users_stats", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap_or_return()
        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        try:
            response = self.session.get(
                f"{self.url}/users/stats", headers=headers, timeout=self.timeout
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="get_users_stats"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def get_users(self, verbose: Optional[bool] = False) -> Result[Response, Error]:
        """

        Returns all users you have created, sorted by creation date in descending order.

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result object with Response object [requests library] if Success
        """
        print_intro("get_users", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap_or_return()
        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        try:
            response = self.session.get(
                f"{self.url}/users", headers=headers, timeout=self.timeout
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="get_users"))

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def get_users_status(
        self,
        verbose: Optional[bool] = False,
        page: int = 1,
        page_size: int = 10,
        descending: bool = True,
        authorized: bool = False,
        sort_by: Union[str, None] = None,
        filter_field: Union[str, None] = None,
        filter_value: Union[str, None] = None,
    ) -> Result[Response, Error]:
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
            A Result object with Response object [requests library] if Success
        """
        print_intro("get_users_status", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap_or_return()
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

        try:
            response = self.session.get(
                f"{self.url}/users/status{url_query_params}",
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="get_users_status"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def add_user_feedback(
        self,
        user_id: str,
        document_id: str,
        selfie_media_id: str,
        decision: Decision,
        additional_feedback: List[str] = [],
        verbose: Optional[bool] = False,
    ) -> Result[Response, Error]:
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
            A Result object with Response object [requests library] if Success
        """
        print_intro("add_user_feedback", verbose=verbose)

        backend_token = self.auth.create_backend_token(user_id).unwrap_or_return()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)

        data = {
            "document_id": document_id,
            "selfie_media_id": selfie_media_id,
            "decision": decision.value,
            "additional_feedback": additional_feedback,
        }

        try:
            response = self.session.post(
                self.url + "/user/feedback",
                data=data,
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="add_user_feedback"))

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def add_selfie(
        self,
        user_id: str,
        media_data: bytes,
        wait_for_completion: Optional[bool] = True,
        verbose: Optional[bool] = False,
    ) -> Result[Response, Error]:
        """

        This call is used to upload for the first time the video of the user's face to the onboarding service.
        This video will be used to extract the biometric face profile.

        Parameters
        ----------
        user_id
            User identifier
        media_data
            Binary media data.
        wait_for_completion
            This setting specifies whether or not the request should return immediately or wait for the operation to complete before returning.
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result object with Response object [requests library] if Success
        """
        print_intro("add_selfie", verbose=verbose)

        user_token = self.auth.create_user_token(user_id).unwrap_or_return()
        print_token("user_token", user_token, verbose=verbose)

        headers = self._auth_headers(user_token)

        files = {"video": ("video", media_data)}

        try:
            response = self.session.post(
                f"{self.url}/user/selfie",
                files=files,
                data={"wait_for_completion": wait_for_completion},
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="add_selfie"))

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def delete_selfie(
        self,
        user_id: str,
        selfie_id: Optional[str] = None,
        verbose: Optional[bool] = False,
    ) -> Result[Response, Error]:
        """

        This call is used to delete the video of the user's face to the onboarding service.
        This will also erase the biometric face profile.

        Parameters
        ----------
        user_id
            User identifier
        selfie_id
            Optional selfie identifier
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result object with Response object [requests library] if Success
        """
        print_intro("delete_selfie", verbose=verbose)

        backend_token = self.auth.create_backend_token(user_id).unwrap_or_return()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        try:
            if not selfie_id:
                response = self.session.delete(
                    f"{self.url}/user/selfie", headers=headers, timeout=self.timeout
                )
            else:
                response = self.session.delete(
                    f"{self.url}/user/selfie/{selfie_id}",
                    headers=headers,
                    timeout=self.timeout,
                )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="delete_selfie"))

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def void_selfie(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, Error]:
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
            A Result object with Response object [requests library] if Success
        """
        print_intro("void_selfie", verbose=verbose)

        backend_token = self.auth.create_backend_token(user_id).unwrap_or_return()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)

        try:
            response = self.session.patch(
                f"{self.url}/user/selfie", headers=headers, timeout=self.timeout
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="void_selfie"))

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def supported_documents(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, Error]:
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
            A Result object with Response object [requests library] if Success
        """
        print_intro("supported_documents", verbose=verbose)

        if user_id:
            token = self.auth.create_user_token(user_id).unwrap_or_return()
            print_token("user_token", token, verbose=verbose)
        else:
            token = self.auth.create_backend_token().unwrap_or_return()
            print_token("backend_token", token, verbose=verbose)

        headers = self._auth_headers(token)

        try:
            response = self.session.get(
                f"{self.url}/documents/supported", headers=headers, timeout=self.timeout
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="supported_documents"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def create_document(
        self,
        user_id: str,
        type: DocumentType,
        issuing_country: str,
        verbose: Optional[bool] = False,
    ) -> Result[Response, Error]:
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
            A Result object with Response object [requests library] if Success
        """
        print_intro("create_document", verbose=verbose)
        user_token = self.auth.create_user_token(user_id).unwrap_or_return()
        print_token("user_token", user_token, verbose=verbose)

        headers = self._auth_headers(user_token)

        data = {"type": type.value, "issuing_country": issuing_country}
        try:
            response = self.session.post(
                f"{self.url}/user/document",
                data=data,
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="create_document"))

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def delete_document(
        self, user_id: str, document_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, Error]:
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
            A Result object with Response object [requests library] if Success
        """
        print_intro("delete_document", verbose=verbose)

        backend_token = self.auth.create_backend_token(user_id).unwrap_or_return()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        try:
            response = self.session.delete(
                f"{self.url}/user/document/{document_id}",
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="delete_document"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def void_document(
        self, user_id: str, document_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, Error]:
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
            A Result object with Response object [requests library] if Success
        """
        print_intro("void_document", verbose=verbose)

        backend_token = self.auth.create_backend_token(user_id).unwrap_or_return()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        try:
            response = self.session.patch(
                f"{self.url}/user/document/{document_id}",
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="void_document"))

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def add_document(
        self,
        user_id: str,
        document_id: str,
        media_data: bytes,
        side: DocumentSide,
        manual: bool = False,
        source: DocumentSource = DocumentSource.file,
        bounding_box: Union[BoundingBox, None] = None,
        fields: Union[Dict[str, Any], None] = None,
        verbose: Optional[bool] = False,
    ) -> Result[Response, Error]:
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
        bounding_box
            Document bounding box. If provided, input image will be cropped according to this region of interest.
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result object with Response object [requests library] if Success
        """
        print_intro("add_document", verbose=verbose)

        user_token = self.auth.create_user_token(user_id).unwrap_or_return()
        print_token("user_token", user_token, verbose=verbose)

        headers = self._auth_headers(user_token)
        data = {
            "document_id": document_id,
            "side": side.value,
            "manual": manual,
            "fields": json.dumps(fields),
            "source": source.value,
        }

        if bounding_box:
            data["bounding_box"] = bounding_box.json()

        files = {"image": ("image", media_data)}

        try:
            response = self.session.put(
                f"{self.url}/user/document",
                files=files,
                data=data,
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="add_document"))

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def document_properties(
        self,
        user_id: str,
        type: DocumentType,
        issuing_country: str,
        verbose: Optional[bool] = False,
    ) -> Result[Response, Error]:
        """

        Returns the properties of a previously added document, such as face, MRZ or NFC availability


        Parameters
        ----------
        user_id
            User identifier
        type
            Type of document [idcard, driverlicense, passport, residencepermit, healthinsurancecard]
        issuing_country
            Issuing Country [ESP, FRA]. Country codes following ISO 3166-1.
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result object with Response object [requests library] if Success
        """
        print_intro("document_properties", verbose=verbose)

        user_token = self.auth.create_user_token(user_id).unwrap_or_return()
        print_token("user_token", user_token, verbose=verbose)

        headers = self._auth_headers(user_token)
        data = {"type": type.value, "issuing_country": issuing_country}

        try:
            response = self.session.post(
                f"{self.url}/user/document/properties",
                data=data,
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="document_properties"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def delete_other_trusted_document(
        self, user_id: str, document_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, Error]:
        """

        Delete all the stored/extracted information from an other trusted document


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
            A Result object with Response object [requests library] if Success
        """
        print_intro("delete_other_trusted_document", verbose=verbose)

        backend_token = self.auth.create_backend_token(user_id).unwrap_or_return()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        try:
            response = self.session.delete(
                f"{self.url}/user/other-trusted-document/{document_id}",
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(
                OnboardingError.timeout(operation="delete_other_trusted_document")
            )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def void_other_trusted_document(
        self, user_id: str, document_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, Error]:
        """

        Mark other trusted document as invalid.


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
            A Result object with Response object [requests library] if Success
        """
        print_intro("void_other_trusted_document", verbose=verbose)

        backend_token = self.auth.create_backend_token(user_id).unwrap_or_return()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)
        try:
            response = self.session.patch(
                f"{self.url}/user/other-trusted-document/{document_id}",
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(
                OnboardingError.timeout(operation="void_other_trusted_document")
            )
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def add_other_trusted_document(
        self,
        user_id: str,
        media_data: bytes,
        category: Optional[str] = None,
        verbose: Optional[bool] = False,
    ) -> Result[Response, Error]:
        """

        This call is used to upload an other trusted document (OTD) to the onboarding service.
        An OTD could be a bank receipt, a proof of address, a bill...
        From a given pdf media, the platform automatically saves the content.

        Parameters
        ----------
        user_id
            User identifier
        media_data
            Binary media data (pdf).
        category
            Optional value to identify an Other Trusted Document (e.g invoice)
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result object with Response object [requests library] if Success
        """
        print_intro("add_other_trusted_document", verbose=verbose)

        user_token = self.auth.create_user_token(user_id).unwrap_or_return()
        print_token("user_token", user_token, verbose=verbose)

        headers = self._auth_headers(user_token)
        files = {"pdf": ("pdf", media_data)}

        data = dict(category=category) if category else dict()

        try:
            response = self.session.post(
                f"{self.url}/user/other-trusted-document",
                files=files,
                data=data,
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(
                OnboardingError.timeout(operation="add_other_trusted_document")
            )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @timeit
    def create_report(
        self,
        user_id: str,
        version: Version = Version.DEFAULT,
        verbose: Optional[bool] = False,
    ) -> Result[Response, Error]:
        """

        This call is used to get the report of the onboarding process for a specific user.
        It returns information on all evidence that has been added and analyzed for that user,
        including documents and facial verifications.


        Parameters
        ----------
        user_id
            User identifier
        version
            Set Report Version
        verbose
            Used for print service response as well as the time elapsed

        Returns
        -------
              A Result object with Response object [requests library] if Success
        """
        print_intro("create_report", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(
            user_id=user_id
        ).unwrap_or_return()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)
        headers["Alice-Report-Version"] = version.value

        try:
            response = self.session.get(
                f"{self.url}/user/report", headers=headers, timeout=self.timeout
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="create_report"))

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def create_certificate(
        self,
        user_id: str,
        locale: CertificateLocale = CertificateLocale.EN,
        template_name: str = "default",
        verbose: Optional[bool] = False,
    ) -> Result[Response, Error]:
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
        locale
            The language of the certificate
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
              A Result object with Response object [requests library] if Success
        """
        print_intro("create_certificate", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(
            user_id=user_id
        ).unwrap_or_return()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        options = {"template_name": template_name, "locale": locale.value}
        headers = self._auth_headers(backend_user_token)
        headers["Content-Type"] = "application/json"
        try:
            response = self.session.post(
                f"{self.url}/user/certificate",
                data=json.dumps(options),
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="create_certificate"))

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def retrieve_certificate(
        self, user_id: str, certificate_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, Error]:
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
              A Result object with Response object [requests library] if Success
        """
        print_intro("retrieve_certificate", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(
            user_id=user_id
        ).unwrap_or_return()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)
        headers = self._auth_headers(backend_user_token)
        try:
            response = self.session.get(
                f"{self.url}/user/certificate/{certificate_id}",
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="retrieve_certificate"))

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def retrieve_certificates(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, Error]:
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
              A Result object with Response object [requests library] if Success
        """
        print_intro("retrieve_certificates", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(
            user_id=user_id
        ).unwrap_or_return()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)
        headers = self._auth_headers(backend_user_token)
        try:
            response = self.session.get(
                f"{self.url}/user/certificates", headers=headers, timeout=self.timeout
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="retrieve_certificates"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def screening(
        self, user_id: str, detail: bool = False, verbose: Optional[bool] = False
    ) -> Result[Response, Error]:
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
              A Result object with Response object [requests library] if Success
        """
        print_intro("screening", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(
            user_id=user_id
        ).unwrap_or_return()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)
        headers = self._auth_headers(backend_user_token)

        url = f"{self.url}/user/screening/search"
        if detail:
            url += "/detail"

        try:
            response = self.session.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="screening"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def screening_monitor_add(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, Error]:
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
              A Result object with Response object [requests library] if Success
        """
        print_intro("screening_monitor_add", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(
            user_id=user_id
        ).unwrap_or_return()
        print_token(
            "backend_token_with_user",
            backend_user_token,
            verbose=verbose,
        )
        headers = self._auth_headers(backend_user_token)

        try:
            response = self.session.post(
                f"{self.url}/user/screening/monitor",
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="screening_monitor_add"))

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def screening_monitor_delete(
        self, user_id: str, verbose: bool = False
    ) -> Result[Response, Error]:
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
              A Result object with Response object [requests library] if Success
        """
        print_intro("screening_monitor_delete", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(
            user_id=user_id
        ).unwrap_or_return()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)
        headers = self._auth_headers(backend_user_token)

        try:
            response = self.session.delete(
                f"{self.url}/user/screening/monitor",
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(
                OnboardingError.timeout(operation="screening_monitor_delete")
            )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def get_monitoring_alerts(
        self, user_id: str, verbose: bool = False
    ) -> Result[Response, Error]:
        """
        Retrieves from the monitoring list the users with open alerts

        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
              A Result object with Response object [requests library] if Success
        """
        print_intro("get_monitoring_alerts", verbose=verbose)

        backend_token = self.auth.create_backend_token(
            user_id=user_id
        ).unwrap_or_return()
        print_token("backend_token_with_user", backend_token, verbose=verbose)
        headers = self._auth_headers(backend_token)

        try:
            response = self.session.get(
                f"{self.url}/user/screening/monitor",
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="get_monitoring_alerts"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def identify_user(
        self,
        target_user_id: str,
        probe_user_ids: List[str],
        version: Version = Version.DEFAULT,
        verbose: bool = False,
    ) -> Result[Response, Error]:
        """
        Identifies (1:N matching) a user against a N-length list of users.

        Parameters
        ----------
         target_user_id
            User identifier (Target)
        probe_user_ids
            List of user identifier to match against (N Probes)
        version
            Set Identify Version
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result object with Response object [requests library] if Success
        """
        print_intro("identify_user", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(
            user_id=target_user_id
        ).unwrap_or_return()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)
        headers["Alice-Identify-Version"] = version.value

        data = {"user_ids": probe_user_ids}

        try:
            response = self.session.post(
                f"{self.url}/user/identify",
                headers=headers,
                data=data,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="identify_user"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def enable_authentication(
        self, user_id: str, verbose: bool = False
    ) -> Result[Response, Error]:
        """
        It enables the authentication for a user.

        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result object with Response object [requests library] if Success
        """
        print_intro("enable_authentication", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(
            user_id=user_id
        ).unwrap_or_return()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)
        try:
            response = self.session.post(
                f"{self.url}/user/authentication/enable",
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="enable_authentication"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def disable_authentication(
        self, user_id: str, verbose: bool = False
    ) -> Result[Response, Error]:
        """
        It disables the authentication for a user.

        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result object with Response object [requests library] if Success
        """
        print_intro("disable_authentication", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(
            user_id=user_id
        ).unwrap_or_return()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)
        try:
            response = self.session.post(
                f"{self.url}/user/authentication/disable",
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="disable_authentication"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def authenticate_user(
        self, user_id: str, media_data: bytes, verbose: bool = False
    ) -> Result[Response, Error]:
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
            A Result object with Response object [requests library] if Success
        """
        print_intro("authenticate_user", verbose=verbose)

        user_token = self.auth.create_user_token(user_id=user_id).unwrap_or_return()
        print_token("user_token", user_token, verbose=verbose)

        headers = self._auth_headers(user_token)

        files = {"video": ("video", media_data)}

        try:
            response = self.session.post(
                f"{self.url}/user/authenticate",
                files=files,
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="authenticate_user"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def get_authentications_ids(
        self, user_id: str, verbose: bool = False
    ) -> Result[Response, Error]:
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
            A Result object with Response object [requests library] if Success
        """
        print_intro("get_authentications_ids", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(
            user_id=user_id
        ).unwrap_or_return()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)

        try:
            response = self.session.get(
                f"{self.url}/user/authentications/ids",
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="get_authentications_ids"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def get_authentications(
        self,
        user_id: str,
        page: int = 1,
        page_size: int = 0,
        descending: bool = True,
        version: Version = Version.DEFAULT,
        verbose: bool = False,
    ) -> Result[Response, Error]:
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
        version
            Set Authentication Version
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result object with Response object [requests library] if Success
        """
        print_intro("get_authentications", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(
            user_id=user_id
        ).unwrap_or_return()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)
        headers["Alice-Authentication-Version"] = version.value

        url_query_params = (
            f"?page={str(page)}&page_size={str(page_size)}&descending={str(descending)}"
        )

        try:
            response = self.session.get(
                f"{self.url}/user/authentications" + url_query_params,
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="get_authentications"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def get_authentication(
        self,
        user_id: str,
        authentication_id: str,
        version: Version = Version.DEFAULT,
        verbose: bool = False,
    ) -> Result[Response, Error]:
        """

        Gets a information from a previous authentication using the verification_id

        Parameters
        ----------
        user_id
            User identifier
        authentication_id
            Authentication identifier.
        version
            Set Authentication Version
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result object with Response object [requests library] if Success
        """
        print_intro("get_authentication", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(
            user_id=user_id
        ).unwrap_or_return()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)
        headers["Alice-Authentication-Version"] = version.value

        try:
            response = self.session.get(
                f"{self.url}/user/authentication/{authentication_id}",
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="get_authentication"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def retrieve_media(
        self, user_id: str, media_id: str, verbose: bool = False
    ) -> Result[Response, Error]:
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
            A Result object with Response object [requests library] if Success
        """
        print_intro("retrieve_media", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(
            user_id=user_id
        ).unwrap_or_return()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)

        try:
            response = self.session.get(
                f"{self.url}/media/{media_id}/download",
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="retrieve_media"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def download(
        self, user_id: str, href: str, verbose: bool = False
    ) -> Result[Response, Error]:
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
             A Result object with Response object [requests library] if Success
        """
        print_intro("download", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(
            user_id=user_id
        ).unwrap_or_return()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)

        try:
            response = self.session.get(href, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="download"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def request_duplicates_search(
        self,
        start_date: datetime,
        end_date: datetime,
        resource_type: DuplicatesResourceType,
        verbose: bool = False,
    ) -> Result[Response, Error]:
        """

        Returns the binary data of a media resource

        Parameters
        ----------
        start_date
            Beginning datetime of the temporal window
        end_date
            Ending datetime of the temporal window
        resource_type
            Entity to analyze (selfie or document)
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library] if success
        """
        print_intro("request_duplicates_search", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap_or_return()
        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)

        data = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "resource_type": resource_type.value,
        }
        try:
            response = self.session.post(
                f"{self.url}/duplicates/search",
                data=data,
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(
                OnboardingError.timeout(operation="request_duplicates_search")
            )
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def get_duplicates_search(
        self, search_id: str, verbose: bool = False
    ) -> Result[Response, Error]:
        """

        Retrieves a previously requested duplicates search from the onboarding platform

        Parameters
        ----------
        search_id
            Duplicates search unique identifier
        verbose
            Used for print service response as well as the time elapsed



        Returns
        -------
            A Response object [requests library] if success
        """
        print_intro("get_duplicates_search", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap_or_return()
        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)

        try:
            response = self.session.get(
                f"{self.url}/duplicates/search/{search_id}",
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="get_duplicates_search"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def get_duplicates_searches(self, verbose: bool = False) -> Result[Response, Error]:
        """

        Retrieves all previously requested duplicates searches from the onboarding platform

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed



        Returns
        -------
            A Response object [requests library]
        """
        print_intro("get_duplicates_searches", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap_or_return()
        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)

        try:
            response = self.session.get(
                f"{self.url}/duplicates/searches", headers=headers, timeout=self.timeout
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="get_duplicates_searches"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @timeit
    def get_user_state(
        self,
        user_id: str,
        verbose: bool = False,
    ) -> Result[Response, Error]:
        """
        Retrieves the state of a user

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
        print_intro("get_user_state", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(
            user_id=user_id
        ).unwrap_or_return()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)
        try:
            response = self.session.get(
                f"{self.url}/user/state",
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="get_user_state"))

        print_response(response=response, verbose=verbose)

        return Success(response)

    @timeit
    def update_user_state(
        self,
        user_id: str,
        user_state: UserState,
        operator: str = "auto",
        update_reasons: Optional[List[Dict[str, str]]] = None,
        verbose: bool = False,
    ) -> Result[Response, Error]:
        """
        Update the state of a user

        Parameters
        ----------
        user_state
            New State of the user
        user_id
            User identifier
        operator
            Who is accepting the user
        update_reasons
            List of reasons for status update
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("update_user_state", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(
            user_id=user_id
        ).unwrap_or_return()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)
        try:
            response = self.session.patch(
                f"{self.url}/user/state",
                headers=headers,
                json={
                    "state": user_state.value,
                    "update_reasons": update_reasons,
                    "operator": operator,
                },
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="update_user_state"))

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def retrieve_flow(
        self, flow_id: Union[str, None] = None, verbose: bool = False
    ) -> Result[Response, Error]:
        """

        Retrieves flow from the onboarding platform

        Parameters
        ----------
        flow_id
            Flow identifier (if none return default flow)
        verbose
            Used for print service response as well as the time elapsed
        Returns
        -------
            A Response object [requests library]
        """
        print_intro("retrieve_flow", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap_or_return()
        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)

        url = f"{self.url}/flow"
        if flow_id:
            url = f"{self.url}/flow?flow_id={flow_id}"

        try:
            response = self.session.get(
                url,
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="retrieve_flow"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def retrieve_flows(self, verbose: bool = False) -> Result[Response, Error]:
        """

        Retrieve flows from the onboarding platform

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed
        Returns
        -------
            A Response object [requests library]
        """
        print_intro("retrieve_flows", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap_or_return()
        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)

        try:
            response = self.session.get(
                f"{self.url}/flows",
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="retrieve_flows"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def create_flow(
        self,
        steps: List[OnboardingSteps],
        default: bool,
        name: str,
        id_: Union[str, None] = None,
        verbose: bool = False,
    ) -> Result[Response, Error]:
        """

        Creates flow

        Parameters
        ----------
        steps
            List of tests that include the flow
        default
            Set the flow as default for all new client users
        name
            The name of the flow
        id_
            UUID for the flow [Optional]
        verbose
            Used for print service response as well as the time elapsed
        Returns
        -------
            A Response object [requests library]
        """
        print_intro("create_flow", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap_or_return()
        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)

        data = {
            "default": default,
            "name": name,
            "steps": [step.value for step in steps],
        }

        if id_:
            data.update({"id": id_})

        try:
            response = self.session.post(
                f"{self.url}/flow",
                headers=headers,
                json=data,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="create_flow"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def update_flow(
        self,
        flow_id: str,
        steps: List[OnboardingSteps],
        default: bool,
        name: str,
        verbose: bool = False,
    ) -> Result[Response, Error]:
        """

        Updates flow

        Parameters
        ----------
        flow_id
            Flow identifier
        steps
            List of tests that include the flow
        default
            Set the flow as default for all new client users
        name
            The name of the flow
        verbose
            Used for print service response as well as the time elapsed
        Returns
        -------
            A Response object [requests library]
        """
        print_intro("update_flow", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap_or_return()
        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)

        data = {
            "id": flow_id,
            "default": default,
            "name": name,
            "steps": [step.value for step in steps],
        }

        try:
            response = self.session.patch(
                f"{self.url}/flow",
                headers=headers,
                json=data,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="update_flow"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def delete_flow(
        self,
        flow_id: str,
        verbose: bool = False,
    ) -> Result[Response, Error]:
        """

        Deletes flow

        Parameters
        ----------
        flow_id
            Flow identifier
        verbose
            Used for print service response as well as the time elapsed
        Returns
        -------
            A Response object [requests library]
        """
        print_intro("delete_flow", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap_or_return()
        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)

        try:
            response = self.session.delete(
                f"{self.url}/flow?flow_id={flow_id}",
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="delete_flow"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def get_user_flow(
        self,
        user_id: str,
        verbose: bool = False,
    ) -> Result[Response, Error]:
        """

        Gets the user flow

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
        print_intro("update_user_flow", verbose=verbose)

        backend_token = self.auth.create_backend_token(user_id).unwrap_or_return()
        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)

        try:
            response = self.session.get(
                f"{self.url}/user/flow",
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="get_user_flow"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def update_user_flow(
        self,
        flow_id: str,
        user_id: str,
        verbose: bool = False,
    ) -> Result[Response, Error]:
        """

        Updates the user flow

        Parameters
        ----------
        flow_id
            Flow identifier
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed
        Returns
        -------
            A Response object [requests library]
        """
        print_intro("update_user_flow", verbose=verbose)

        backend_token = self.auth.create_backend_token(user_id).unwrap_or_return()
        print_token("backend_token", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)

        try:
            response = self.session.patch(
                f"{self.url}/user/flow/{flow_id}",
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="update_user_flow"))
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def request(
        self,
        func: Callable[[RequestRunner], Response],
        user_id: Union[str, None] = None,
        verbose: bool = False,
    ) -> Result[Response, Error]:
        print_intro("request", verbose=verbose)

        token = self.auth.create_backend_token(user_id).unwrap_or_return()
        print_token("backend_token", token, verbose=verbose)

        headers = self._auth_headers(token)

        try:
            response = func(
                RequestRunner(
                    session=self.session,
                    headers=headers,
                    base_url=self.url,
                    timeout=self.timeout,
                )
            )

        except requests.exceptions.Timeout:
            return Failure(OnboardingError.timeout(operation="request"))
        print_response(response=response, verbose=verbose)

        return Success(response)
