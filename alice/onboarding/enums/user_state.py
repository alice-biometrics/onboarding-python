from enum import Enum


class UserState(Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    TO_REVIEW = "TO_REVIEW"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
