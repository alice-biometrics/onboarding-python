from enum import Enum


class Environment(str, Enum):
    SANDBOX = "sandbox"
    PRODUCTION = "production"
    STAGING = "staging"
