from typing import List, Optional

from pydantic import BaseModel, Field

from alice.onboarding.models.report_v1.checks.check import Check
from alice.onboarding.models.report_v1.compliance.device_out import DeviceOut
from alice.onboarding.models.report_v1.document.document_field import ReportV1Field
from alice.onboarding.models.report_v1.face_matching.face_matching import FaceMatching
from alice.onboarding.models.report_v1.summary.external_user_data import (
    ExternalUserData,
)


class ReportSummary(BaseModel):
    """
    It summarizes the main user information of the onboarding process
    """

    face_liveness: float = Field(
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
    user_data: Optional[List[ReportV1Field]] = Field(
        default=[], description="Best read user-intrinsic info across all docs"
    )
    external_user_data: Optional[ExternalUserData] = None
    devices: List[DeviceOut] = Field(
        default=[], description="Devices operated by the user"
    )
