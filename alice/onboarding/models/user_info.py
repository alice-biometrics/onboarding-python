from typing import Optional

from pydantic import BaseModel


class UserInfo(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
