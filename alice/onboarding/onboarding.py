from typing import List, Dict

from meiga import Result, Success, Failure, isSuccess

from alice.config import Config
from alice.onboarding.decision import Decision
from alice.onboarding.document_source import DocumentSource
from alice.onboarding.onboarding_errors import OnboardingError
from alice.onboarding.user_info import UserInfo
from alice.onboarding.device_info import DeviceInfo
from alice.onboarding.onboarding_client import OnboardingClient
from alice.auth.auth import Auth

DEFAULT_URL = "https://apis.alicebiometrics.com/onboarding"


class Onboarding:
    @staticmethod
    def from_config(config: Config):
        return Onboarding(
            auth=Auth.from_config(config),
            url=config.onboarding_url,
            send_agent=config.send_agent,
        )

    def __init__(self, auth: Auth, url: str = DEFAULT_URL, send_agent: bool = True):
        self.onboarding_client = OnboardingClient(
            auth=auth, url=url, send_agent=send_agent
        )
        self.url = url

    def healthcheck(self, verbose: bool = False) -> Result[bool, OnboardingError]:
        """
        Runs a healthcheck on the service to see if there are any problems.

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.healthcheck(verbose=verbose)

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="healthcheck", response=response
                )
            )

    def create_user(
        self,
        user_info: UserInfo = None,
        device_info: DeviceInfo = None,
        verbose: bool = False,
    ) -> Result[str, OnboardingError]:
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
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.create_user(
            user_info=user_info, device_info=device_info, verbose=verbose
        )

        if response.status_code == 200:
            return Success(response.json()["user_id"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="create_user", response=response
                )
            )

    def delete_user(
        self, user_id: str, verbose: bool = False
    ) -> Result[bool, OnboardingError]:
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
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.delete_user(user_id=user_id, verbose=verbose)

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="delete_user", response=response
                )
            )

    def get_user_status(
        self, user_id: str, verbose: bool = False
    ) -> Result[Dict, OnboardingError]:
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
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.get_user_status(
            user_id=user_id, verbose=verbose
        )

        if response.status_code == 200:
            return Success(response.json()["user"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="get_user_status", response=response
                )
            )

    def get_users(self, verbose: bool = False) -> Result[List[str], OnboardingError]:
        """

        Returns all users you have created, sorted by creation date in descending order.

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns list of string with already created user_ids.
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.get_users()

        if response.status_code == 200:
            return Success(response.json()["users"])
        else:
            return Failure(
                OnboardingError.from_response(operation="get_users", response=response)
            )

    def get_users_stats(self, verbose: bool = False) -> Result[Dict, OnboardingError]:
        """

        Returns statistics about users in the Onboarding platform.

        Parameters
        ----------
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns a dict with users information
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.get_users_stats(verbose=verbose)

        if response.status_code == 200:
            return Success(response.json()["stats"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="get_users_stats", response=response
                )
            )

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
    ) -> Result[List[Dict[str, str]], OnboardingError]:
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
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.get_users_status(
            verbose=verbose,
            page=page,
            page_size=page_size,
            descending=descending,
            authorized=authorized,
            sort_by=sort_by,
            filter_field=filter_field,
            filter_value=filter_value,
        )

        if response.status_code == 200:
            return Success(response.json())
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="get_users_status", response=response
                )
            )

    def add_user_feedback(
        self,
        user_id: str,
        document_id: str,
        selfie_media_id: str,
        decision: Decision,
        additional_feedback: List[str] = [],
        verbose: bool = False,
    ) -> Result[bool, OnboardingError]:
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
            Otherwise, it returns an OnboardingError.
        """

        response = self.onboarding_client.add_user_feedback(
            user_id=user_id,
            document_id=document_id,
            selfie_media_id=selfie_media_id,
            decision=decision,
            additional_feedback=additional_feedback,
            verbose=verbose,
        )

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="add_user_feedback", response=response
                )
            )

    def add_selfie(
        self, user_id: str, media_data: bytes, verbose: bool = False
    ) -> Result[bool, OnboardingError]:
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
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.add_selfie(
            user_id=user_id, media_data=media_data, verbose=verbose
        )

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(operation="add_selfie", response=response)
            )

    def delete_selfie(
        self, user_id: str, verbose: bool = False
    ) -> Result[bool, OnboardingError]:
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
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.delete_selfie(
            user_id=user_id, verbose=verbose
        )

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="delete_selfie", response=response
                )
            )

    def void_selfie(
        self, user_id: str, verbose: bool = False
    ) -> Result[bool, OnboardingError]:
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
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.void_selfie(user_id=user_id, verbose=verbose)

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="void_selfie", response=response
                )
            )

    def supported_documents(
        self, user_id: str = None, verbose: bool = False
    ) -> Result[Dict[str, str], OnboardingError]:
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
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.supported_documents(
            user_id=user_id, verbose=verbose
        )
        if response.status_code == 200:
            return Success(response.json())
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="supported_documents", response=response
                )
            )

    def create_document(
        self, user_id: str, type: str, issuing_country: str, verbose: bool = False
    ) -> Result[str, OnboardingError]:
        """

        This call is used to obtain a new document_id
        With this document_id you will be able to extract information with the add_document method

        Parameters
        ----------
        user_id
            User identifier
        type
            Type of document [idcard, driverlicense, passport, residencepermit]
        issuing_country
            Issuing Country [ESP, FRA]. Country codes following ISO 3166-1.

        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns a str with a document_id.
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.create_document(
            user_id=user_id, type=type, issuing_country=issuing_country, verbose=verbose
        )

        if response.status_code == 200:
            return Success(response.json()["document_id"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="create_document", response=response
                )
            )

    def delete_document(
        self, user_id: str, document_id: str, verbose: bool = False
    ) -> Result[bool, OnboardingError]:
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
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.delete_document(
            user_id=user_id, document_id=document_id, verbose=verbose
        )

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="delete_document", response=response
                )
            )

    def void_document(
        self, user_id: str, document_id: str, verbose: bool = False
    ) -> Result[bool, OnboardingError]:
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
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.void_document(
            user_id=user_id, document_id=document_id, verbose=verbose
        )

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="void_document", response=response
                )
            )

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
    ) -> Result[bool, OnboardingError]:
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
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns True.
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.add_document(
            user_id=user_id,
            document_id=document_id,
            media_data=media_data,
            side=side,
            manual=manual,
            source=source,
            fields=fields,
            verbose=verbose,
        )

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="add_document", response=response
                )
            )

    def document_properties(
        self, user_id: str, document_id: str, verbose: bool = False
    ) -> Result[str, OnboardingError]:
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
            A Result where if the operation is successful it returns dict with document properties.
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.document_properties(
            user_id=user_id, document_id=document_id, verbose=verbose
        )

        if response.status_code == 200:
            return Success(response.json())
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="document_properties", response=response
                )
            )

    def create_report(
        self, user_id: str, verbose: bool = False
    ) -> Result[Dict, OnboardingError]:
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
            A Result where if the operation is successful it returns a Dict with the generated report.
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.create_report(
            user_id=user_id, verbose=verbose
        )

        if response.status_code == 200:
            return Success(response.json()["report"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="create_report", response=response
                )
            )

    def create_certificate(
        self, user_id: str, template_name: str = "default", verbose: bool = False
    ) -> Result[Dict, OnboardingError]:
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
            A Result where if the operation is successful it returns a str with a pdf_report_id.
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.create_certificate(
            user_id=user_id, template_name=template_name, verbose=verbose
        )

        if response.status_code == 200:
            return Success(response.json()["certificate_id"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="create_certificate", response=response
                )
            )

    def retrieve_certificate(
        self, user_id: str, certificate_id: str, verbose: bool = False
    ) -> Result[bytes, OnboardingError]:
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
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.retrieve_certificate(
            user_id=user_id, certificate_id=certificate_id, verbose=verbose
        )

        if response.status_code == 200:
            return Success(response.content)
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="retrieve_certificate", response=response
                )
            )

    def retrieve_certificates(
        self, user_id: str, verbose: bool = False
    ) -> Result[List, OnboardingError]:
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
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.retrieve_certificates(
            user_id=user_id, verbose=verbose
        )

        if response.status_code == 200:
            return Success(response.json()["certificates"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="retrieve_certificates", response=response
                )
            )

    def screening(
        self, user_id: str, detail: bool = False, verbose: bool = False
    ) -> Result[List, OnboardingError]:
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
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.screening(
            user_id=user_id, detail=detail, verbose=verbose
        )

        if response.status_code == 200:
            return Success(response.json()["screening_result"])
        else:
            return Failure(
                OnboardingError.from_response(operation="screening", response=response)
            )

    def screening_monitor_add(
        self, user_id: str, verbose: bool = False
    ) -> Result[List, OnboardingError]:
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
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.screening_monitor_add(
            user_id=user_id, verbose=verbose
        )

        if response.status_code == 201:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="screening_monitor_add", response=response
                )
            )

    def screening_monitor_delete(
        self, user_id: str, verbose: bool = False
    ) -> Result[List, OnboardingError]:
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
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.screening_monitor_delete(
            user_id=user_id, verbose=verbose
        )

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="screening_monitor_delete", response=response
                )
            )

    def screening_monitor_open_alerts(
        self, start_index: int = 0, size: int = 100, verbose: bool = False
    ) -> Result[bool, OnboardingError]:
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
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.screening_monitor_open_alerts(
            start_index=start_index, size=size, verbose=verbose
        )

        if response.status_code == 200:
            return Success(response.json())
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="screening_monitor_open_alerts", response=response
                )
            )

    def identify_user(
        self, target_user_id: str, probe_user_ids: List[str], verbose: bool = False
    ) -> Result[bool, OnboardingError]:
        """
        Identifies (1:N matching) a user against a N-lenght list of users.

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
            A Result where if the operation is successful it returns a dict with sorted users by face score.
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.identify_user(
            target_user_id=target_user_id,
            probe_user_ids=probe_user_ids,
            verbose=verbose,
        )
        if response.status_code == 200:
            return Success(response.json())
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="identify_user", response=response
                )
            )

    def authorize_user(
        self, user_id: str, verbose: bool = False
    ) -> Result[bool, OnboardingError]:
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
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.authorize_user(
            user_id=user_id, verbose=verbose
        )

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="authorize_user", response=response
                )
            )

    def deauthorize_user(
        self, user_id: str, verbose: bool = False
    ) -> Result[bool, OnboardingError]:
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
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.deauthorize_user(
            user_id=user_id, verbose=verbose
        )

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="deauthorize_user", response=response
                )
            )

    def authenticate_user(
        self, user_id: str, media_data: bytes, verbose: bool = False
    ) -> Result[str, OnboardingError]:
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
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.authenticate_user(
            user_id=user_id, media_data=media_data, verbose=verbose
        )

        if response.status_code == 200:
            return Success(response.json()["authentication_id"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="authenticate_user", response=response
                )
            )

    def get_authentications_ids(
        self, user_id: str, verbose: bool = False
    ) -> Result[List[str], OnboardingError]:
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
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.get_authentications_ids(
            user_id=user_id, verbose=verbose
        )

        if response.status_code == 200:
            return Success(response.json()["authentication_ids"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="get_authentications_ids", response=response
                )
            )

    def get_authentications(
        self,
        user_id: str,
        page: int = 1,
        page_size: int = 0,
        descending: bool = True,
        verbose: bool = False,
    ) -> Result[List[Dict], OnboardingError]:
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


        Returns
        -------
            A Result where if the operation is successful it returns a Dictionary with a List of authentications and
            the total number of authentications.
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.get_authentications(
            user_id=user_id,
            page_size=page_size,
            page=page,
            descending=descending,
            verbose=verbose,
        )

        if response.status_code == 200:
            return Success(response.json())
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="get_authentications", response=response
                )
            )

    def get_authentication(
        self, user_id: str, authentication_id: str, verbose: bool = False
    ) -> Result[Dict, OnboardingError]:
        """

        Returns the result of a authentication given a authentication_id

        Parameters
        ----------
        user_id
            User identifier
        authentication_id
            Authentication identifier
        verbose
            Used for print service response as well as the time elapsed


        Returns
        -------
            A Result where if the operation is successful it returns a Dict with the information of one authentication.
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.get_authentication(
            user_id=user_id, authentication_id=authentication_id, verbose=verbose
        )

        if response.status_code == 200:
            return Success(response.json()["authentication"])
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="get_authentication", response=response
                )
            )

    def retrieve_media(
        self, user_id: str, media_id: str, verbose: bool = False
    ) -> Result[bytes, OnboardingError]:
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
            Otherwise, it returns an OnboardingError.
        """
        response = self.onboarding_client.retrieve_media(
            user_id=user_id, media_id=media_id, verbose=verbose
        )

        if response.status_code == 200:
            return Success(response.content)
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="retrieve_media", response=response
                )
            )
