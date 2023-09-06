from typing import Union

from pydantic import BaseModel, Field


class DocumentSideReportMeta(BaseModel):
    """
    It collects document side metadata
    """

    template: Union[str, None] = Field(
        default=None, description="Document version used to extract the info"
    )
    manual: Union[bool, None] = Field(
        default=None, description="True if the capture was taken in manual mode"
    )
