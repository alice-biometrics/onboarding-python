# coding=utf-8
# Copyright (C) 2019+ Alice, Vigo, Spain

"""Public API of Alice Onboarding Python SDK"""

# Modules
from alice.webhooks.webhook import Webhook
from alice.webhooks.webhooks import Webhooks
from alice.webhooks.webhooks_client import WebhooksClient

modules = []

from alice.auth.auth import Auth
from alice.auth.auth_client import AuthClient
from alice.config import Config
from alice.onboarding.enums.decision import Decision
from alice.onboarding.enums.document_side import DocumentSide
from alice.onboarding.enums.document_source import DocumentSource
from alice.onboarding.enums.document_type import DocumentType
from alice.onboarding.enums.version import Version
from alice.onboarding.models.bounding_box import BoundingBox
from alice.onboarding.models.device_info import DeviceInfo
from alice.onboarding.models.user_info import UserInfo

# Classes
from alice.onboarding.onboarding import Onboarding
from alice.onboarding.onboarding_client import OnboardingClient
from alice.sandbox.sandbox import Sandbox
from alice.sandbox.sandbox_client import SandboxClient

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
    "Webhooks",
    "WebhooksClient",
    "Webhook",
    "Decision",
    "DocumentType",
    "Version",
    "DocumentSide",
    "DocumentSource",
    "BoundingBox",
]


# Errors
from alice.onboarding.onboarding_errors import OnboardingError
from alice.sandbox.sandbox_errors import SandboxError

errors = ["OnboardingError", "SandboxError"]

__all__ = modules + classes + errors
