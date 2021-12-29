import os

from setuptools import setup

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PACKAGE_NAME = "alice-onboarding"
VERSION = open("alice/VERSION", "r").read()

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
        "alice/auth",
        "alice/sandbox",
        "alice/webhooks",
    ],
    zip_safe=False,
    install_requires=REQUIRES,
    include_package_data=True,
)
