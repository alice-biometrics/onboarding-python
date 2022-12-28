from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from meiga import Failure, Result, Success, early_return, isSuccess
from requests import Session

from alice.auth.auth import Auth
from alice.auth.auth_errors import AuthError
from alice.config import Config
from alice.onboarding.enums.certificate_locale import CertificateLocale
from alice.onboarding.enums.decision import Decision
from alice.onboarding.enums.document_side import DocumentSide
from alice.onboarding.enums.document_source import DocumentSource
from alice.onboarding.enums.document_type import DocumentType
from alice.onboarding.enums.duplicates_resource_type import DuplicatesResourceType
from alice.onboarding.enums.version import Version
from alice.onboarding.models.bounding_box import BoundingBox
from alice.onboarding.models.device_info import DeviceInfo
from alice.onboarding.models.report.report import Report
from alice.onboarding.models.user_info import UserInfo
from alice.onboarding.onboarding_client import OnboardingClient
from alice.onboarding.onboarding_errors import OnboardingError

DEFAULT_URL = "https://apis.alicebiometrics.com/onboarding"


class Onboarding:
    @staticmethod
    def from_config(config: Config) -> "Onboarding":
        if config.session:
            session = config.session
        else:
            session = Session()
        return Onboarding(
            auth=Auth.from_config(config),
            url=config.onboarding_url,
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
        verbose: bool = False,
    ):
        self.onboarding_client = OnboardingClient(
            auth=auth, url=url, send_agent=send_agent, session=session
        )
        self.url = url
        self.verbose = verbose

    @early_return
    def healthcheck(
        self, verbose: Optional[bool] = False
    ) -> Result[bool, Union[OnboardingError, AuthError]]:
        """
        Runs a healthcheck on the service to see if there are any problems.

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
        response = self.onboarding_client.healthcheck(
            verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="healthcheck", response=response
                )
            )

    @early_return
    def create_user(
        self,
        user_info: Union[UserInfo, None] = None,
        device_info: Union[DeviceInfo, None] = None,
        verbose: Optional[bool] = False,
    ) -> Result[str, Union[OnboardingError, AuthError]]:
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
            A Result where if the operation is successful it returns a user_id.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.create_user(
            user_info=user_info, device_info=device_info, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json()["user_id"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="create_user", response=response
                )
            )

    @early_return
    def delete_user(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Result[bool, Union[OnboardingError, AuthError]]:
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
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.delete_user(
            user_id=user_id, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="delete_user", response=response
                )
            )

    @early_return
    def get_user_status(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Result[Dict[str, Any], Union[OnboardingError, AuthError]]:
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
            A Result where if the operation is successful it returns a Dict with the status info.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.get_user_status(
            user_id=user_id, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json()["user"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="get_user_status", response=response
                )
            )

    @early_return
    def get_users(
        self, verbose: Optional[bool] = False
    ) -> Result[List[str], Union[OnboardingError, AuthError]]:
        """

        Returns all users you have created, sorted by creation date in descending order.

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns list of string with already created user_ids.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.get_users(verbose=verbose).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json()["users"])
        else:
            return Failure(
                OnboardingError.from_response(operation="get_users", response=response)
            )

    @early_return
    def get_users_stats(
        self, verbose: Optional[bool] = False
    ) -> Result[Dict[str, Any], Union[OnboardingError, AuthError]]:
        """

        Returns statistics about users in the Onboarding platform.

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns a dict with users information
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.get_users_stats(
            verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json()["stats"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="get_users_stats", response=response
                )
            )

    @early_return
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
    ) -> Result[List[Dict[str, str]], Union[OnboardingError, AuthError]]:
        """

        Returns every UserStatus available for all the Users in the onboarding platform ordered by creation date.

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed
        page
            Page from which users will be returned. Default 1.
        page_size
            Numbers of users per page that will be returned. To return all the users select 0.
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
            A Result where if the operation is successful it returns list of dict which represent the status of each user.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.get_users_status(
            verbose=verbose,
            page=page,
            page_size=page_size,
            descending=descending,
            authorized=authorized,
            sort_by=sort_by,
            filter_field=filter_field,
            filter_value=filter_value,
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json())
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="get_users_status", response=response
                )
            )

    @early_return
    def add_user_feedback(
        self,
        user_id: str,
        document_id: str,
        selfie_media_id: str,
        decision: Decision,
        additional_feedback: List[str] = [],
        verbose: Optional[bool] = False,
    ) -> Result[bool, Union[OnboardingError, AuthError]]:
        """

        This call is used to add client's feedback on user onboarding. Usually, it is given after human review.

        Parameters
        ----------
        user_id
            User identifier
        document_id
            Document identifier.
        selfie_media_id
            Selfie media identifier.
        decision
            Whether user is accepted or rejected ["OK", "KO-client", "KO-alice"]
        additional_feedback
            List of strings containing additional feedback on user onboarding
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.add_user_feedback(
            user_id=user_id,
            document_id=document_id,
            selfie_media_id=selfie_media_id,
            decision=decision,
            additional_feedback=additional_feedback,
            verbose=verbose,
        ).unwrap_or_return()

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="add_user_feedback", response=response
                )
            )

    @early_return
    def add_selfie(
        self, user_id: str, media_data: bytes, verbose: Optional[bool] = False
    ) -> Result[bool, Union[OnboardingError, AuthError]]:
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
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.add_selfie(
            user_id=user_id, media_data=media_data, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(operation="add_selfie", response=response)
            )

    @early_return
    def delete_selfie(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Result[bool, Union[OnboardingError, AuthError]]:
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
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.delete_selfie(
            user_id=user_id, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="delete_selfie", response=response
                )
            )

    @early_return
    def void_selfie(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Result[bool, Union[OnboardingError, AuthError]]:
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
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.void_selfie(
            user_id=user_id, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="void_selfie", response=response
                )
            )

    @early_return
    def supported_documents(
        self, user_id: Union[str, None] = None, verbose: Optional[bool] = False
    ) -> Result[Dict[str, str], Union[OnboardingError, AuthError]]:
        """
        This method is used to obtain a hierarchical-ordered dict with the information of the documents supported by the API.

        This method can be called accessed with both USER_TOKEN and BACKEND_TOKEN.
        If you provide a user_id this method call it using the USER_TOKEN, otherwise it will be called with the BACKEND_TOKEN

        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns dict with supported document.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.supported_documents(
            user_id=user_id, verbose=verbose
        ).unwrap_or_return()
        if response.status_code == 200:
            return Success(response.json())
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="supported_documents", response=response
                )
            )

    @early_return
    def create_document(
        self,
        user_id: str,
        type: DocumentType,
        issuing_country: str,
        verbose: Optional[bool] = False,
    ) -> Result[str, Union[OnboardingError, AuthError]]:
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
            Issuing Country [ESP, FRA]. Country codes following ISO 3166-1.

        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns a str with a document_id.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.create_document(
            user_id=user_id, type=type, issuing_country=issuing_country, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json()["document_id"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="create_document", response=response
                )
            )

    @early_return
    def delete_document(
        self, user_id: str, document_id: str, verbose: Optional[bool] = False
    ) -> Result[bool, Union[OnboardingError, AuthError]]:
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
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.delete_document(
            user_id=user_id, document_id=document_id, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="delete_document", response=response
                )
            )

    @early_return
    def void_document(
        self, user_id: str, document_id: str, verbose: Optional[bool] = False
    ) -> Result[bool, Union[OnboardingError, AuthError]]:
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
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.void_document(
            user_id=user_id, document_id=document_id, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="void_document", response=response
                )
            )

    @early_return
    def add_document(
        self,
        user_id: str,
        document_id: str,
        media_data: bytes,
        side: DocumentSide,
        manual: bool = False,
        source: DocumentSource = DocumentSource.file,
        fields: Union[Dict[str, Any], None] = None,
        bounding_box: Union[BoundingBox, None] = None,
        verbose: Optional[bool] = False,
    ) -> Result[bool, Union[OnboardingError, AuthError]]:
        """

        Deletes all the information

        Parameters
        ----------
        user_id
            User identifier
        document_id
            Document identifier
        media_data
            Binary media data.
        side
            Side of the document [front, back or internal]
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
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.add_document(
            user_id=user_id,
            document_id=document_id,
            media_data=media_data,
            side=side,
            manual=manual,
            source=source,
            fields=fields,
            bounding_box=bounding_box,
            verbose=verbose,
        ).unwrap_or_return()

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="add_document", response=response
                )
            )

    @early_return
    def document_properties(
        self,
        user_id: str,
        type: DocumentType,
        issuing_country: str,
        verbose: Optional[bool] = False,
    ) -> Result[str, Union[OnboardingError, AuthError]]:
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
            A Result where if the operation is successful it returns dict with document properties.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.document_properties(
            user_id=user_id, type=type, issuing_country=issuing_country, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json())
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="document_properties", response=response
                )
            )

    @early_return
    def add_other_trusted_document(
        self,
        user_id: str,
        pdf: bytes,
        category: Optional[str] = None,
        verbose: Optional[bool] = False,
    ) -> Result[bool, Union[OnboardingError, AuthError]]:
        """

        It uploads an other trusted document (OTD) to the onboarding service.
        An OTD could be a bank receipt, a proof of address, a bill... in pdf format.

        Parameters
        ----------
        user_id
            User identifier
        pdf
            Binary media data of pdf file.
        category
            Optional value to identify an Other Trusted Document (e.g invoice)
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns a str with a document_id.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.add_other_trusted_document(
            user_id=user_id,
            media_data=pdf,
            category=category,
            verbose=verbose,
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json()["document_id"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="add_other_trusted_document", response=response
                )
            )

    @early_return
    def delete_other_trusted_document(
        self, user_id: str, document_id: str, verbose: Optional[bool] = False
    ) -> Result[bool, Union[OnboardingError, AuthError]]:
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
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.delete_other_trusted_document(
            user_id=user_id, document_id=document_id, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="delete_other_trusted_document", response=response
                )
            )

    @early_return
    def void_other_trusted_document(
        self, user_id: str, document_id: str, verbose: Optional[bool] = False
    ) -> Result[bool, Union[OnboardingError, AuthError]]:
        """

        Mark an other trusted document as invalid.


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
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.void_other_trusted_document(
            user_id=user_id, document_id=document_id, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="void_other_trusted_document", response=response
                )
            )

    @early_return
    def create_report(
        self,
        user_id: str,
        version: Version = Version.DEFAULT,
        raw: Optional[bool] = False,
        verbose: Optional[bool] = False,
    ) -> Result[Union[Report, Dict[str, Any]], Union[OnboardingError, AuthError]]:
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
        raw
            Whether to return the report as a Dict or as a Report object
        verbose
            Used for print service response as well as the time elapsed

        Returns
        -------
            A Result where if the operation is successful it returns a Report object if raw=True or Dict otherwise.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.create_report(
            user_id=user_id, version=version, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            report_dict = response.json()["report"]
            if report_dict["version"] == 1 and not raw:
                return Success(Report.parse_obj(report_dict))
            else:
                return Success(report_dict)
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="create_report", response=response
                )
            )

    @early_return
    def create_certificate(
        self,
        user_id: str,
        template_name: str = "default",
        locale: CertificateLocale = CertificateLocale.EN,
        verbose: Optional[bool] = False,
    ) -> Result[str, Union[OnboardingError, AuthError]]:
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
            A Result where if the operation is successful it returns a str with a certificate_id.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.create_certificate(
            user_id=user_id, template_name=template_name, locale=locale, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json()["certificate_id"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="create_certificate", response=response
                )
            )

    @early_return
    def retrieve_certificate(
        self, user_id: str, certificate_id: str, verbose: Optional[bool] = False
    ) -> Result[bytes, Union[OnboardingError, AuthError]]:
        """

        Returns the binary data of an existent pdf report

        Parameters
        ----------
        user_id
            User identifier
        certificate_id
           Certificate Unique Identifier. You can obtain it using create_certificate method.
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns a binary pdf (bytes).
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.retrieve_certificate(
            user_id=user_id, certificate_id=certificate_id, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.content)
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="retrieve_certificate", response=response
                )
            )

    @early_return
    def retrieve_certificates(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Result[List[Dict[str, Any]], Union[OnboardingError, AuthError]]:
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
            A Result where if the operation is successful it returns a list of dictionaries.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.retrieve_certificates(
            user_id=user_id, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json()["certificates"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="retrieve_certificates", response=response
                )
            )

    @early_return
    def screening(
        self, user_id: str, detail: bool = False, verbose: Optional[bool] = False
    ) -> Result[List[Dict[str, Any]], Union[OnboardingError, AuthError]]:
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
            A Result where if the operation is successful it returns a dictionary.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.screening(
            user_id=user_id, detail=detail, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json()["screening_result"])
        else:
            return Failure(
                OnboardingError.from_response(operation="screening", response=response)
            )

    @early_return
    def screening_monitor_add(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Result[bool, OnboardingError]:
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
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.screening_monitor_add(
            user_id=user_id, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 201:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="screening_monitor_add", response=response
                )
            )

    @early_return
    def screening_monitor_delete(
        self, user_id: str, verbose: Optional[bool] = False
    ) -> Result[bool, Union[OnboardingError, AuthError]]:
        """

        This call is deletes a user from the AML monitoring list.

        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed

        Returns
        -------
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.screening_monitor_delete(
            user_id=user_id, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="screening_monitor_delete", response=response
                )
            )

    @early_return
    def screening_monitor_open_alerts(
        self, start_index: int = 0, size: int = 100, verbose: bool = False
    ) -> Result[bool, Union[OnboardingError, AuthError]]:
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
            A Result where if the operation is successful it returns a dictionary.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.screening_monitor_open_alerts(
            start_index=start_index, size=size, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json())
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="screening_monitor_open_alerts", response=response
                )
            )

    @early_return
    def identify_user(
        self,
        target_user_id: str,
        probe_user_ids: List[str],
        version: Version = Version.DEFAULT,
        verbose: bool = False,
    ) -> Result[bool, Union[OnboardingError, AuthError]]:
        """
        Identifies (1:N matching) a user against a N-lenght list of users.

        Parameters
        ----------
        target_user_id
            User identifier (Target)
        probe_user_ids
            List of user identifier to match against (N Probes)
        version
            Set Identify version
        verbose
            Used for print service response as well as the time elapsed
        Returns
        -------
            A Result where if the operation is successful it returns a dict with sorted users by face score.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.identify_user(
            target_user_id=target_user_id,
            probe_user_ids=probe_user_ids,
            version=version,
            verbose=verbose,
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json())
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="identify_user", response=response
                )
            )

    @early_return
    def authorize_user(
        self, user_id: str, verbose: bool = False
    ) -> Result[bool, Union[OnboardingError, AuthError]]:
        """
        Authorizes a user. Now it can be icated.
        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed
        Returns
        -------
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.authorize_user(
            user_id=user_id, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="authorize_user", response=response
                )
            )

    @early_return
    def deauthorize_user(
        self, user_id: str, verbose: bool = False
    ) -> Result[bool, Union[OnboardingError, AuthError]]:
        """
        Deauthorizes a user. Now it cannot be authenticated.

        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.deauthorize_user(
            user_id=user_id, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="deauthorize_user", response=response
                )
            )

    @early_return
    def authenticate_user(
        self, user_id: str, media_data: bytes, verbose: bool = False
    ) -> Result[str, Union[OnboardingError, AuthError]]:
        """

        Authenticate a previously registered User against a given media to verify the identity

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
            A Result where if the operation is successful it returns a authentication_id.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.authenticate_user(
            user_id=user_id, media_data=media_data, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json()["authentication_id"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="authenticate_user", response=response
                )
            )

    @early_return
    def get_authentications_ids(
        self, user_id: str, verbose: bool = False
    ) -> Result[List[str], Union[OnboardingError, AuthError]]:
        """

        Returns all authentications ids you have performed for a User, sorted by creation date in descending order.

        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns a List of string with all the authentication_ids.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.get_authentications_ids(
            user_id=user_id, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json()["authentication_ids"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="get_authentications_ids", response=response
                )
            )

    @early_return
    def get_authentications(
        self,
        user_id: str,
        page: int = 1,
        page_size: int = 0,
        descending: bool = True,
        version: Version = Version.DEFAULT,
        verbose: bool = False,
    ) -> Result[List[Dict[str, Any]], Union[OnboardingError, AuthError]]:
        """

        Returns all authentications you have performed for a User.

        Parameters
        ----------
        user_id
            User identifier
        verbose
            Used for print service response as well as the time elapsed
        page
            Page from which authentications will be returned. Default 1.
        page_size
            Numbers of authentications per page that will be returned. To return all the authentications select 0.
        descending
            Order of the authentications according to their creation date.
        version
            Set Authentication Version
        verbose
            Used for print service response as well as the time elapsed

        Returns
        -------
            A Result where if the operation is successful it returns a Dictionary with a List of authentications and
            the total number of authentications.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.get_authentications(
            user_id=user_id,
            page_size=page_size,
            page=page,
            descending=descending,
            version=version,
            verbose=verbose,
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json())
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="get_authentications", response=response
                )
            )

    @early_return
    def get_authentication(
        self,
        user_id: str,
        authentication_id: str,
        version: Version = Version.DEFAULT,
        verbose: bool = False,
    ) -> Result[Dict[str, Any], Union[OnboardingError, AuthError]]:
        """

        Returns the result of a authentication given a authentication_id

        Parameters
        ----------
        user_id
            User identifier
        authentication_id
            Authentication identifier
        version
            Set Authentication Version
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns a Dict with the information of one authentication.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.get_authentication(
            user_id=user_id,
            authentication_id=authentication_id,
            version=version,
            verbose=verbose,
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json()["authentication"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="get_authentication", response=response
                )
            )

    @early_return
    def retrieve_media(
        self, user_id: str, media_id: str, verbose: bool = False
    ) -> Result[bytes, Union[OnboardingError, AuthError]]:
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
            A Result where if the operation is successful it returns a binary image (bytes).
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.retrieve_media(
            user_id=user_id, media_id=media_id, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.content)
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="retrieve_media", response=response
                )
            )

    @early_return
    def download(
        self, user_id: str, href: str, verbose: bool = False
    ) -> Result[bytes, Union[OnboardingError, AuthError]]:
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
            A Result where if the operation is successful it returns a binary object (bytes).
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.download(
            user_id=user_id, href=href, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.content)
        else:
            return Failure(
                OnboardingError.from_response(operation="download", response=response)
            )

    @early_return
    def request_duplicates_search(
        self,
        start_date: datetime,
        end_date: datetime,
        resource_type: DuplicatesResourceType,
        verbose: bool = False,
    ) -> Result[str, Union[OnboardingError, AuthError]]:
        """

        Requests a duplicates search to the onboarding platform

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
            A Result where if the operation is successful it returns a search_id.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.request_duplicates_search(
            start_date=start_date,
            end_date=end_date,
            resource_type=resource_type,
            verbose=verbose,
        ).unwrap_or_return()

        if response.status_code == 202:
            return Success(response.json()["search_id"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="request_duplicates_search", response=response
                )
            )

    @early_return
    def get_duplicates_search(
        self, search_id: str, verbose: bool = False
    ) -> Result[Dict[str, Any], Union[OnboardingError, AuthError]]:
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
            A Result where if the operation is successful it returns the duplicates result.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.get_duplicates_search(
            search_id=search_id, verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json())
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="get_duplicates_search", response=response
                )
            )

    @early_return
    def get_duplicates_searches(
        self, verbose: bool = False
    ) -> Result[List[Dict[str, Any]], Union[OnboardingError, AuthError]]:
        """

        Retrieves a previously requested duplicates search from the onboarding platform

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns the duplicates result.
            Otherwise, it returns an OnboardingError or AuthError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.get_duplicates_searches(
            verbose=verbose
        ).unwrap_or_return()

        if response.status_code == 200:
            return Success(response.json()["searches"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="get_duplicates_searches", response=response
                )
            )

    def accept_user(
        self, user_id: str, verbose: bool = False
    ) -> Result[bool, OnboardingError]:
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
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.accept_user(user_id=user_id, verbose=verbose)

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="accept_user", response=response
                )
            )

    def reject_user(
        self,
        user_id: str,
        rejection_reasons: Optional[List[Dict[str, str]]] = None,
        verbose: bool = False,
    ) -> Result[bool, OnboardingError]:
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
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError.
        """
        verbose = self.verbose or verbose
        response = self.onboarding_client.reject_user(
            user_id=user_id, rejection_reasons=rejection_reasons, verbose=verbose
        )

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="accept_user", response=response
                )
            )
