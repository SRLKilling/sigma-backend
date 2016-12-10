Sigma - Backend
===============

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/ProjetSigma/backend/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/ProjetSigma/backend/?branch=master)
[![Circle CI](https://circleci.com/gh/ProjetSigma/backend.svg?style=svg)](https://circleci.com/gh/ProjetSigma/backend)
[![Coverage Status](https://coveralls.io/repos/github/ProjetSigma/backend/badge.svg?branch=master)](https://coveralls.io/github/ProjetSigma/backend?branch=master)

## Licence
<a href="https://github.com/ProjetSigma/backend/blob/master/LICENSE.md">
<img src="https://img.shields.io/badge/license-GNU%20Affero%20General%20Public%20License%20%28AGPL%29%20v3.0-blue.svg" alt="license" />
</a>


Vagrant usage
-------------
If you want to use the vagrant setup, you don't have to install python libraries.  
Please see the [provisioning repository](https://github.com/ProjetSigma/provisioning).

Installation
------------

**Requirements.**  
On Debian-based distribution, you will need the following librairies:
```[sh]
apt-get install python-dev libmysqlclient-dev libjpeg-dev python3.5-dev
```

**Python 3 is required.**  
We recommend to use a virtualenv for python.

Follow these instructions to setup the project.

First, configure the manager editing the settings.py file.
You'll need to provide the name of your python and pip programs.
If you're on a campus, you can also add a proxy setting.

Then, install dependances  
`manage.py install`

Finally, initialize the database, and load static files
`manage.py init`

Usage
-----

The `manage.py` file provides some useful tools. Here is how to use it :

To start the data server, i.e. the one containing the database/django stuff
`manage.py run-data-server`

To start the notification server, i.e. the one which clients will open websockets to, use
`manage.py run-data-server`

To use the Django manager, simply use `manage.py django [...]` followed by the parameters you want to use
For example you could do `manage.py django migrate`

Fixtures
--------

If you'd like to test things out, fill the database with some random fixtures using
`manage.py fixtures`
You'll be provided with a super-user :
```
Email: admin@sigma.fr
Password: admin
```

An OAuth client application is also created (see below for further information), with data:
* `clientId`: `bJeSCIWpvjbYCuXZNxMzVz0wglX8mHR2ZTKHxaDv`
* `clientSecret`: `XjbfZS6Apq05PDTSL4CoFHGo7NsKVAa1XMVrVElk5N1t0dOSyqxrHPff6okAi6X6Du9XxrK4dl0mLQ0YlscJsjnL5IKhQagQdGv2SgumhYRFaMi6LtHNPXicmMr8oLdy`




OAuth usage
-----------

###Create an application *(temporary)*
NB. For frontend usage only, you can skip this part.

When you are logged in, you can create a trusted application at: `http://127.0.0.1:8000/o/applications/`  

I still have to understand how to deal correctly with applications addition... :p

For the name, put whatever you want. Choose **Client Type**: *confidential* and **Authorization Grant Type**: *Resource owner password-based*.

###Get your token
`client_id` and `client_secret` depend on the trusted application. To get token, do:  
`curl -X POST -d "grant_type=password&username=<user_name>&password=<password>" -u"<client_id>:<client_secret>" http://127.0.0.1:8000/o/token/`

The answer should be:
```json
{
    "access_token": "<your_access_token>",
    "token_type": "Bearer",
    "expires_in": 36000,
    "refresh_token": "<your_refresh_token>",
    "scope": "read write groups"
}
```

###Visit the secured API
With your token, you can access the secured API by passing an *Authorization* token in your request:  
`curl -H "Authorization: Bearer <your_access_token>" http://127.0.0.1:8000/user/`
