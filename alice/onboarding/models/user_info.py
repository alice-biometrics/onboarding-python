from typing import Optional

from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
