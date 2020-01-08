from typing import Optional

from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class UserInfo:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None


e = UserInfo().to_dict()
