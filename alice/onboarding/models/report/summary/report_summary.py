from typing import List, Union

from pydantic import BaseModel, Field

from alice.onboarding.models.report.checks.check import Check
from alice.onboarding.models.report.compliance.device_out import DeviceOut
from alice.onboarding.models.report.document.document_field import ReportV1Field
from alice.onboarding.models.report.face_matching.face_matching import FaceMatching
from alice.onboarding.models.report.shared.entity_result import EntityResult
from alice.onboarding.models.report.summary.external_user_data import ExternalUserData
from alice.onboarding.models.report.summary.report_user_state import ReportUserState


class UserResult(BaseModel):
    """
    It summarizes the result of the onboarding process
    """

    selfie_security: EntityResult = Field(default=EntityResult.NA, description="")
    document_security: EntityResult = Field(default=EntityResult.NA, description="")
    document_read: EntityResult = Field(default=EntityResult.NA, description="")
    process_security: EntityResult = Field(default=EntityResult.NA, description="")


class ReportSummary(BaseModel):
    """
    It summarizes the main user information of the onboarding process
    """

    result: UserResult = Field(default=UserResult(), description="")
    face_liveness: Union[float, None] = Field(
        default=None,
        ge=0,
        le=100,
        description="Analysis to detect if the user's active selfie is from a real person. The recommended threshold is 50.",
    )
    face_matching: List[FaceMatching] = Field(
        default=[],
        description="All available face matchings between user's seflies and docs",
    )
    checks: List[Check] = Field(default=[], description="Summary/User-level checks")
    user_data: Union[List[ReportV1Field], None] = Field(
        default=[], description="Best read user-intrinsic info across all docs"
    )
    external_user_data: Union[ExternalUserData, None] = None
    sessions: int = Field(
        default=0, description="Total number of user sessions in the SDK"
    )
    sessions_until_first_succeeded_onboarding: Union[int, None] = Field(
        default=None,
        description="Number of sessions the user needed to complete the onboarding process for the first time",
    )
    devices: List[DeviceOut] = Field(
        default=[], description="Devices operated by the user"
    )
    state: Union[ReportUserState, None] = None
