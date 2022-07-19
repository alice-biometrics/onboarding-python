from typing import Dict, Optional

from pydantic import Field
from pydantic.main import BaseModel

from alice.onboarding.models.report.shared.bounding_box import BoundingBox


class Href(BaseModel):
    """
    It collects info about a media resource
    """

    href: str = Field(description="HTML-like href link")
    extension: Optional[str] = Field(default=None, description="Media extension")
    objects: Optional[Dict[str, BoundingBox]] = Field(
        defualt=None, description="Identified regions"
    )
