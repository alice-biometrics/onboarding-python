from pydantic import BaseModel, Field


class DocumentSideReportMeta(BaseModel):
    """
    It collects document side metadata
    """

    template: str = Field(
        default=None, description="Document version used to extract the info"
    )
    manual: bool = Field(
        default=None, description="True if the capture was taken in manual mode"
    )
