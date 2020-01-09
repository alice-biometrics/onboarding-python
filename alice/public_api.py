# coding=utf-8
# Copyright (C) 2019+ Alice, Vigo, Spain

"""Public API of ALiCE Onboarding Python SDK"""

# Modules

modules = []

# Classes
from alice.onboarding.onboarding import Onboarding
from alice.onboarding.onboarding_client import OnboardingClient
from alice.onboarding.user_info import UserInfo
from alice.onboarding.device_info import DeviceInfo
from alice.auth.auth import Auth
from alice.auth.auth_client import AuthClient
from alice.sandbox.sandbox import Sandbox
from alice.sandbox.sandbox_client import SandboxClient
from alice.config import Config


classes = [
    "Onboarding",
    "OnboardingClient",
    "UserInfo",
    "DeviceInfo",
    "Auth",
    "AuthClient",
    "Sandbox",
    "SandboxClient",
    "Config",
]

# Errors
from alice.onboarding.onboarding_errors import OnboardingError
from alice.sandbox.sandbox_errors import SandboxError

errors = ["OnboardingError", "SandboxError"]

__all__ = modules + classes + errors
