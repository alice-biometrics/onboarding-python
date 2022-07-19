from typing import Optional

from pydantic.main import BaseModel


class ExternalUserData(BaseModel):
    """
    It collects the given data at user creation time
    """

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
