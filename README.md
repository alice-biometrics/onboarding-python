ALiCE Onboarding API Python Client
==================================


Install from PyPI:

```console
pip install alice-onboarding
```

Install from code:

```console
git clone https://github.com/alice-biometrics/onboarding-api-python-client.git
pip install -e .
```

To install to develop:

```console
conda create --name onboarding-sdk python=3.6
conda activate onboarding-sdk
pip install .
```

## Upload to internal PyPi


#### Quick way

1. Update version in setup.py
2. Execute the following command

```console
bash deploy_wheel.sh
```

#### Step by step

Create dist folder:

```console
python setup.py sdist bdist_wheel
```


To upload it use twine

First of all, install it
```console
pip install twine
```

Then, upload created wheel
```console
twine upload dist/* --repository-url https://intranet.gradiant.org/nexus/repository/pypi-biometrics/    
```


Another way to create a wheel

```console
pip wheel --wheel-dir=output/package .
pip install output/package/alice_onboarding-*-py3-none-any
```

## Usage

Default (Using PRO)

```python
from alice import OnboardingSdk, AuthSdk

API_KEY = "<ADD-YOUR-API-KEY>"

auth_sdk = AuthSdk(api_key=API_KEY)
onboarding_sdk = OnboardingSdk(auth_sdk=auth_sdk)

ok = onboarding_sdk.healthcheck(verbose=True)
assert ok, "healthcheck is not returning a 200"
```

Parametrized (e.g Using PRE)

```python
from alice import OnboardingSdk, AuthSdk

auth_sdk = AuthSdk(
    service_id="onboarding", base_url="https://pre.alicebiometrics.com/auth", api_key="<ADD-YOUR-API-KEY>"
)
onboarding_sdk = OnboardingSdk(auth_sdk=auth_sdk, url="https://pre.alicebiometrics.com/onboarding")

ok = onboarding_sdk.healthcheck(verbose=True)
assert ok, "healthcheck is not returning a 200"
```

## Documentation

Dependencies

```console
pip instal Sphinx
pip install sphinx_rtd_theme
```

Generate html

```console
cd docs
make html
```
