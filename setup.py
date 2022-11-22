import os

from setuptools import setup

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PACKAGE_NAME = "alice-onboarding"
VERSION = open("alice/VERSION").read()

with open(os.path.join(CURRENT_DIR, "README.md")) as fid:
    README = fid.read()

with open("requirements/requirements.txt") as f:
    REQUIRES = f.read().splitlines()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    long_description=README,
    long_description_content_type="text/markdown",
    keywords=["onboarding", "biometrics", "kyc", "alice"],
    description="Alice Onboarding Python SDK",
    url="https://github.com/alice-biometrics/onboarding-python",
    author="Alice Biometrics",
    author_email="support@alicebiometrics.com",
    license="Alice Copyright",
    packages=[
        "alice",
        "alice/onboarding",
        "alice/onboarding/enums",
        "alice/onboarding/models",
        "alice/onboarding/models/report",
        "alice/onboarding/models/report/checks",
        "alice/onboarding/models/report/checks/document",
        "alice/onboarding/models/report/checks/field",
        "alice/onboarding/models/report/checks/selfie",
        "alice/onboarding/models/report/checks/summary",
        "alice/onboarding/models/report/compliance",
        "alice/onboarding/models/report/document",
        "alice/onboarding/models/report/face_matching",
        "alice/onboarding/models/report/other_trusted_document",
        "alice/onboarding/models/report/selfie",
        "alice/onboarding/models/report/shared",
        "alice/onboarding/models/report/summary",
        "alice/auth",
        "alice/sandbox",
        "alice/webhooks",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        # "Programming Language :: Python :: 3.11", # TODO
    ],
    zip_safe=False,
    install_requires=REQUIRES,
    include_package_data=True,
)
