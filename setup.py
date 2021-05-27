from setuptools import setup

VERSION = open("alice/VERSION", "r").read()
REQUIRES = [
    "pyjwt==2.1.0",
    "requests>=2.18.0",
    "dataclasses>=0.6",
    "dataclasses-json>=0.2.14",
    "meiga==1.2.12",
]

setup(
    name="alice-onboarding",
    version=VERSION,
    description="Alice Onboarding Python SDK",
    url="https://alicebiometrics.com",
    author="ALiCE Biometrics",
    author_email="support@alicebiometrics.com",
    license="ALiCE Copyright",
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
