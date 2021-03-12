# onboarding-python <img src="https://github.com/alice-biometrics/custom-emojis/blob/master/images/python.png" width="30"> [![version](https://img.shields.io/github/release/alice-biometrics/onboarding-python/all.svg)](https://github.com/alice-biometrics/onboarding-python/releases) [![doc](https://img.shields.io/badge/doc-onboarding-51CB56)](https://docs.alicebiometrics.com/onboarding/sections/server/server_side_sdks/python.html)

<img src="https://github.com/alice-biometrics/custom-emojis/blob/master/images/alice_header.png" width=auto>


The aim of this Python package is to manage the authentication and backend operations against ALiCE Onboarding API.

If you want more information about how to integrate with ALiCE technology, please contact us at support@alicebiometrics.com.

## Table of Contents
- [Requirements](#requirements)
- [Installation :computer:](#installation-computer)
- [Getting Started :chart_with_upwards_trend:](#getting-started-chart_with_upwards_trend)
  * [Config](#config)
  * [Onboarding](#onboarding)
- [Authentication :closed_lock_with_key:](#authentication-closed_lock_with_key)
- [Advanced Features :tophat:](#advanced-features-tophat)
  * [Certified Onboarding](#certified-onboarding)
  * [User Screening](#user-screening)
- [Documentation :page_facing_up:](#documentation-page_facing_up)
- [Contact :mailbox_with_mail:](#contact-mailbox_with_mail)


## Requirements

Python 3.6+

## Installation :computer:

```console
pip install alice-onboarding
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

## Authentication :closed_lock_with_key:

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

## Advanced features :tophat:

:warning: These features could not be available by default. If you obtain a HTTP Error (405 method not allowed). Please, contact us to make them available for your credentials.

#### Certified Onboarding 

If you need certify your user data, you can retrieve a certified Pdf Report with these feature.

```console
export ONBOARDING_API_KEY="<YOUR-API-KEY>"
python examples/onboarding_with_certificate.py
```

see certified onboarding usage [here](examples/onboarding_with_certificate.py)

#### User Screening

ALiCE Onboarding API bring us the opportunity of screening a user over different databases & lists (sanctions, PEP, etc)..

```console
export ONBOARDING_API_KEY="<YOUR-API-KEY>"
python examples/onboarding_with_screening.py
```

see screening onboarding usage [here](examples/onboarding_with_screening.py)


#### Webhooks

Configure your webhooks through the api with the `Webhooks` object. 

```console
export ONBOARDING_API_KEY="<YOUR-API-KEY>"
python examples/onboarding_with_webhooks.py
```

see onboarding webhooks usage [here](examples/onboarding_with_webhooks.py)

Note: You can configure your webhooks using the Onboarding dashboard.

## Documentation :page_facing_up:

For more information about ALiCE Onboarding:  https://docs.alicebiometrics.com/onboarding/

## Contact :mailbox_with_mail:

support@alicebiometrics.com

