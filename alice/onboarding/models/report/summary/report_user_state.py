from typing import Union

from pydantic import BaseModel

from alice.onboarding.enums.user_state import UserState


class ReportUserState(BaseModel):
    value: Union[UserState, None] = None
