import os
import random
import string

import pytest


@pytest.fixture
def given_valid_api_key():
    api_key = os.environ.get("ONBOARDING_API_KEY")
    if api_key is None:
        raise AssertionError(
            "Please configure your ONBOARDING_API_KEY to run the tests"
        )
    return api_key


@pytest.fixture
def given_valid_sandbox_token():
    sandbox_token = os.environ.get("ONBOARDING_SANDBOX_TOKEN")
    if sandbox_token is None:
        raise AssertionError(
            "Please configure your ONBOARDING_SANDBOX_TOKEN to run the tests"
        )
    return sandbox_token


@pytest.fixture
def given_any_valid_mail():
    domains = [
        "hotmail.com",
        "gmail.com",
        "aol.com",
        "mail.com",
        "mail.kz",
        "yahoo.com",
    ]
    letters = string.ascii_lowercase[:12]
    mail = (
        "".join(random.choice(letters) for i in range(7)) + "@" + random.choice(domains)
    )
    return mail


@pytest.fixture
def given_resources_path():
    return f"{os.path.dirname(os.path.abspath(__file__))}/../resources"


@pytest.fixture
def given_any_selfie_image_media_data(given_resources_path):
    with open(f"{given_resources_path}/selfie.png", "rb") as f:
        yield f.read()


@pytest.fixture
def given_any_document_front_media_data(given_resources_path):
    with open(f"{given_resources_path}/idcard_esp_front_example.png", "rb") as f:
        yield f.read()


@pytest.fixture
def given_any_document_back_media_data(given_resources_path):
    with open(f"{given_resources_path}/idcard_esp_back_example.png", "rb") as f:
        yield f.read()


@pytest.fixture
def given_any_pdf_media_data(given_resources_path):
    with open(f"{given_resources_path}/test.pdf", "rb") as f:
        yield f.read()
