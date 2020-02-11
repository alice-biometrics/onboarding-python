# onboarding-python  [![version](https://img.shields.io/github/release/alice-biometrics/onboarding-python/all.svg)](https://github.com/alice-biometrics/onboarding-python/releases) ![ci](https://github.com/alice-biometrics/onboarding-python/workflows/ci/badge.svg)

The aim of this Python package is to manage the authentication and backend operations against ALiCE Onboarding API.

If you want more information about how to integrate with ALiCE technology, please contact us at support@alicebiometrics.com.

## Requirements

Python 3.6+

## Installation :computer:

```console
pip install alice-onboarding
```

Install from code:

```console
pip install git+https://github.com/alice-biometrics/onboarding-python.git
```

## Getting Started :chart_with_upwards_trend:

#### Config 

Configure your credentials with *Config* class

```
from alice import Config

config = Config(api_key=given_valid_api_key)
```


#### Onboarding

To manage the operations with ALiCE Onboarding API, use *Onboarding* class. 
This class deals with authentication automatically.

```console
export ONBOARDING_API_KEY="<YOUR-API-KEY>"
python examples/onboarding.py
```

see onboarding example [here](examples/onboarding.py)

#### Auth

To manage authorization and token creations, use *Auth* class.

Available tokens: 

| Type Token              | Info          | 
| ----------------------- |:-------------:|
| BACKEND_TOKEN           | Used to secure global requests.| 
| BACKEND_TOKEN_WITH_USER | Used to secure global requests include user_id information embedded |  
| USER_TOKEN              | Used to secure requests made by the users on their mobile devices or web clients.|


To create a BACKEND_TOKEN_WITH_USER and a USER_TOKEN you will need a valid user_id obtained from Alice Onboarding API.


```console
export ONBOARDING_API_KEY="<YOUR-API-KEY>"
python examples/auth.py
```

see auth example [here](examples/auth.py)


#### Sandbox (Only for early stages of integration)

To manage the operations with the Sandbox API, use *Sandbox* class.

```console
export ONBOARDING_SANDBOX_TOKEN="<YOUR-SANDBOX-TOKEN>"
python examples/sandbox.py
```

see sandbox example [here](examples/sandbox.py)

