import os

from setuptools import find_packages, setup

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
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    zip_safe=False,
    install_requires=REQUIRES,
    include_package_data=True,
)
