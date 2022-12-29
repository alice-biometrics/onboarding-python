import json
import platform
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import requests
from meiga import Error, Result, Success, early_return
from requests import Response, Session

import alice
from alice.auth.auth import Auth
from alice.auth.auth_errors import AuthError
from alice.onboarding.enums.certificate_locale import CertificateLocale
from alice.onboarding.enums.decision import Decision
from alice.onboarding.enums.document_side import DocumentSide
from alice.onboarding.enums.document_source import DocumentSource
from alice.onboarding.enums.document_type import DocumentType
from alice.onboarding.enums.duplicates_resource_type import DuplicatesResourceType
from alice.onboarding.enums.version import Version
from alice.onboarding.models.bounding_box import BoundingBox
from alice.onboarding.models.device_info import DeviceInfo
from alice.onboarding.models.user_info import UserInfo
from alice.onboarding.tools import print_intro, print_response, print_token, timeit

DEFAULT_URL = "https://apis.alicebiometrics.com/onboarding"


class OnboardingClient:
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

        response = self.session.get(f"{self.url}/healthcheck")

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def create_user(
        self,
        user_info: Union[UserInfo, None] = None,
        device_info: Union[DeviceInfo, None] = None,
        verbose: Optional[bool] = False,
    ) -> Result[Response, AuthError]:
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

        response = self.session.post(f"{self.url}/user", headers=headers, data=data)

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def delete_user(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
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
        response = self.session.delete(f"{self.url}/user", headers=headers)

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def get_user_status(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
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

        response = self.session.get(f"{self.url}/user/status", headers=headers)

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def get_users_stats(
        self, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
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
        response = self.session.get(f"{self.url}/users/stats", headers=headers)

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def get_users(self, verbose: Optional[bool] = False) -> Result[Response, AuthError]:
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
        response = self.session.get(f"{self.url}/users", headers=headers)

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def get_users_status(
        self,
        verbose: Optional[bool] = False,
        page: int = 1,
        page_size: int = 0,
        descending: bool = True,
        authorized: bool = False,
        sort_by: Union[str, None] = None,
        filter_field: Union[str, None] = None,
        filter_value: Union[str, None] = None,
    ) -> Result[Response, AuthError]:
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

        response = self.session.get(
            f"{self.url}/users/status{url_query_params}", headers=headers
        )

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
    ) -> Result[Response, AuthError]:
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

        response = self.session.post(
            self.url + "/user/feedback", data=data, headers=headers
        )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def add_selfie(
        self, user_id: str, media_data: bytes, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
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
            A Result object with Response object [requests library] if Success
        """
        print_intro("add_selfie", verbose=verbose)

        user_token = self.auth.create_user_token(user_id).unwrap_or_return()
        print_token("user_token", user_token, verbose=verbose)

        headers = self._auth_headers(user_token)

        files = {"video": ("video", media_data)}

        response = self.session.post(
            f"{self.url}/user/selfie", files=files, headers=headers
        )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def delete_selfie(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
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
            A Result object with Response object [requests library] if Success
        """
        print_intro("delete_selfie", verbose=verbose)

        backend_token = self.auth.create_backend_token(user_id).unwrap_or_return()
        print_token("backend_token_with_user", backend_token, verbose=verbose)

        headers = self._auth_headers(backend_token)

        response = self.session.delete(f"{self.url}/user/selfie", headers=headers)

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def void_selfie(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
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

        response = self.session.patch(f"{self.url}/user/selfie", headers=headers)

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def supported_documents(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
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

        response = self.session.get(f"{self.url}/documents/supported", headers=headers)
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
    ) -> Result[Response, AuthError]:
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
        response = self.session.post(
            f"{self.url}/user/document", data=data, headers=headers
        )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def delete_document(
        self, user_id: str, document_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
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
        response = self.session.delete(
            f"{self.url}/user/document/{document_id}", headers=headers
        )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def void_document(
        self, user_id: str, document_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
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
        response = self.session.patch(
            f"{self.url}/user/document/{document_id}", headers=headers
        )

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
    ) -> Result[Response, AuthError]:
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

        response = self.session.put(
            f"{self.url}/user/document", files=files, data=data, headers=headers
        )

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
    ) -> Result[Response, AuthError]:
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

        response = self.session.post(
            f"{self.url}/user/document/properties", data=data, headers=headers
        )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def delete_other_trusted_document(
        self, user_id: str, document_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
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
        response = self.session.delete(
            f"{self.url}/user/other-trusted-document/{document_id}", headers=headers
        )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def void_other_trusted_document(
        self, user_id: str, document_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
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
        response = self.session.patch(
            f"{self.url}/user/other-trusted-document/{document_id}", headers=headers
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
    ) -> Result[Response, AuthError]:
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

        response = self.session.post(
            f"{self.url}/user/other-trusted-document",
            files=files,
            data=data,
            headers=headers,
        )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @timeit
    def create_report(
        self,
        user_id: str,
        version: Version = Version.DEFAULT,
        verbose: Optional[bool] = False,
    ) -> Result[Response, AuthError]:
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

        response = self.session.get(f"{self.url}/user/report", headers=headers)

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
    ) -> Result[Response, AuthError]:
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
        response = self.session.post(
            f"{self.url}/user/certificate", data=json.dumps(options), headers=headers
        )
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def retrieve_certificate(
        self, user_id: str, certificate_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
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
        response = self.session.get(
            f"{self.url}/user/certificate/{certificate_id}", headers=headers
        )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def retrieve_certificates(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
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
        response = self.session.get(f"{self.url}/user/certificates", headers=headers)

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def screening(
        self, user_id: str, detail: bool = False, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
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

        response = self.session.get(url, headers=headers)

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def screening_monitor_add(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Result[Response, AuthError]:
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
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)
        headers = self._auth_headers(backend_user_token)

        response = self.session.get(
            f"{self.url}/user/screening/monitor", headers=headers
        )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def screening_monitor_delete(
        self, user_id: str, verbose: bool = False
    ) -> Result[Response, AuthError]:
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

        response = self.session.delete(
            f"{self.url}/user/screening/monitor", headers=headers
        )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def screening_monitor_open_alerts(
        self, start_index: int = 0, size: int = 100, verbose: bool = False
    ) -> Result[Response, AuthError]:
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
              A Result object with Response object [requests library] if Success
        """
        print_intro("screening_monitor_open_alerts", verbose=verbose)

        backend_token = self.auth.create_backend_token().unwrap_or_return()
        print_token("backend_token", backend_token, verbose=verbose)
        headers = self._auth_headers(backend_token)

        response = self.session.get(
            f"{self.url}/users/screening/monitor/alerts?start_index={start_index}&size={size}",
            headers=headers,
        )

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
    ) -> Result[Response, AuthError]:
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

        response = self.session.post(
            f"{self.url}/user/identify", headers=headers, data=data
        )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def authorize_user(
        self, user_id: str, verbose: bool = False
    ) -> Result[Response, AuthError]:
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
            A Result object with Response object [requests library] if Success
        """
        print_intro("authorize_user", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(
            user_id=user_id
        ).unwrap_or_return()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)
        response = self.session.post(f"{self.url}/user/authorize", headers=headers)

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def deauthorize_user(
        self, user_id: str, verbose: bool = False
    ) -> Result[Response, AuthError]:
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
            A Result object with Response object [requests library] if Success
        """
        print_intro("deauthorize_user", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(
            user_id=user_id
        ).unwrap_or_return()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)
        response = self.session.post(f"{self.url}/user/deauthorize", headers=headers)

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def authenticate_user(
        self, user_id: str, media_data: bytes, verbose: bool = False
    ) -> Result[Response, AuthError]:
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

        response = self.session.post(
            f"{self.url}/user/authenticate", files=files, headers=headers
        )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def get_authentications_ids(
        self, user_id: str, verbose: bool = False
    ) -> Result[Response, AuthError]:
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

        response = self.session.get(
            f"{self.url}/user/authentications/ids", headers=headers
        )

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
    ) -> Result[Response, AuthError]:
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

        response = self.session.get(
            f"{self.url}/user/authentications" + url_query_params, headers=headers
        )

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
    ) -> Result[Response, AuthError]:
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

        response = self.session.get(
            f"{self.url}/user/authentication/{authentication_id}", headers=headers
        )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def retrieve_media(
        self, user_id: str, media_id: str, verbose: bool = False
    ) -> Result[Response, AuthError]:
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

        response = self.session.get(
            f"{self.url}/media/{media_id}/download", headers=headers
        )

        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def download(
        self, user_id: str, href: str, verbose: bool = False
    ) -> Result[Response, AuthError]:
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

        response = self.session.get(href, headers=headers)

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
    ) -> Result[Response, AuthError]:
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
        response = requests.post(
            f"{self.url}/duplicates/search", data=data, headers=headers
        )
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def get_duplicates_search(
        self, search_id: str, verbose: bool = False
    ) -> Result[Response, AuthError]:
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

        response = requests.get(
            f"{self.url}/duplicates/search/{search_id}", headers=headers
        )
        print_response(response=response, verbose=verbose)

        return Success(response)

    @early_return
    @timeit
    def get_duplicates_searches(
        self, verbose: bool = False
    ) -> Result[Response, AuthError]:
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

        response = requests.get(f"{self.url}/duplicates/searches", headers=headers)
        print_response(response=response, verbose=verbose)

        return Success(response)

    @timeit
    def accept_user(self, user_id: str, verbose: bool = False) -> Response:
        """
        Mark a user state as ACCEPTED

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
        print_intro("accept_user", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(
            user_id=user_id
        ).unwrap_or_return()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)
        response = requests.post(f"{self.url}/user/state/accept", headers=headers)

        print_response(response=response, verbose=verbose)

        return response

    @timeit
    def reject_user(
        self,
        user_id: str,
        rejection_reasons: Optional[List[Dict[str, str]]] = None,
        verbose: bool = False,
    ) -> Response:
        """
        Mark a user state as REJECTED

        Parameters
        ----------
        user_id
            User identifier
        rejection_reasons
            List of rejection reasons
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Response object [requests library]
        """
        print_intro("accept_user", verbose=verbose)

        backend_user_token = self.auth.create_backend_token(
            user_id=user_id
        ).unwrap_or_return()
        print_token("backend_token_with_user", backend_user_token, verbose=verbose)

        headers = self._auth_headers(backend_user_token)
        response = requests.post(
            f"{self.url}/user/state/reject",
            headers=headers,
            json={"rejection_reasons": rejection_reasons},
        )

        print_response(response=response, verbose=verbose)

        return response
