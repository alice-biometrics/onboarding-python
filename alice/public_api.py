# coding=utf-8
# Copyright (C) 2019+ Alice, Vigo, Spain

"""Public API of ALiCE Onboarding Python SDK"""

# Modules

modules = []

# Classes
from alice.onboarding.onboarding_sdk import OnboardingSdk
from alice.onboarding.onboarding_client import OnboardingClient
from alice.onboarding.user_info import UserInfo
from alice.onboarding.device_info import DeviceInfo
from alice.auth.auth_sdk import AuthSdk
from alice.auth.auth_client import AuthClient
from alice.sandbox.sandbox_sdk import SandboxSdk
from alice.sandbox.sandbox_client import SandboxClient

classes = [
    "OnboardingSdk",
    "OnboardingClient",
    "UserInfo",
    "DeviceInfo",
    "AuthSdk",
    "AuthClient",
    "SandboxSdk",
    "SandboxClient",
]

# Errors
from alice.onboarding.onboarding_errors import OnboardingError
from alice.sandbox.sandbox_errors import SandboxError

errors = ["OnboardingError", "SandboxError"]

__all__ = modules + classes + errors
