from typing import Optional

from pydantic import BaseModel, Field


class Check(BaseModel):
    """
    It examines if a certain condition is met
    """

    key: str = Field(
        description="Unique check identifier",
    )
    value: Optional[float] = Field(
        None, description="this is the value of the check", ge=0, le=100
    )
    detail: Optional[str] = Field(
        None,
        description="Brief check description",
    )
