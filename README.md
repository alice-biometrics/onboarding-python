ALiCE Onboarding API Python Client
==================================

## Installation

Install from PyPI: Not yet available :construction:

```console
pip install alice-onboarding
```

Install from code:

```console
git clone https://github.com/alice-biometrics/onboarding-api-python-client.git
pip install -e .
```

## Getting Started

#### Config 

Configure your credentials with *Config* class

```
from alice import Config

config = Config(api_key=given_valid_api_key)
```


#### Onboarding

To manage the operations with ALiCE Onboarding API, use *Onboarding* class. 
This class deals with authentication automatically.

see onboarding example [here](examples/onboarding.py)

```console
export ONBOARDING_API_KEY="<YOUR-API-KEY>"
python examples/onboarding.py
```

#### Auth

To manage authorization and token creations, use *Auth* class.

see onboarding example [here](examples/auth.py)

```console
export ONBOARDING_API_KEY="<YOUR-API-KEY>"
python examples/auth.py
```

#### Sandbox (Only for early stages of integration)

To manage the operations with the Sandbox API, use *Sandbox* class.

see onboarding example [here](examples/sandbox.py)

```console
export ONBOARDING_SANDBOX_TOKEN="<YOUR-SANDBOX-TOKEN>"
python examples/sandbox.py
```
