from typing import List, Dict

from meiga import Result, Success, Failure, isSuccess

from alice.config import Config
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
                OnboardingError.from_response(operation="add_Selfie", response=response)
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
        response = self.onboarding_client.void_selfie(
            user_id=user_id, verbose=verbose
        )

        if response.status_code == 200:
            return isSuccess
        else:
            return Failure(
                OnboardingError.from_response(
                    operation="void_selfie", response=response
                )
            )

    def supported_documents(
        self, user_id: str, verbose: bool = False
    ) -> Result[Dict[str, str], OnboardingError]:
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

    def authorize_user(
        self, user_id: str, verbose: bool = False
    ) -> Result[bool, OnboardingError]:
        """
        Authorizes a user. Now it can be authenticated.

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
            return Success(response.json()["authentications"])
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
