Sigma - Backend

===============
## Licence
<a href="https://github.com/ProjetSigma/backend/blob/master/LICENSE.md">
<img src="https://img.shields.io/badge/license-GNU%20Affero%20General%20Public%20License%20%28AGPL%29%20v3.0-blue.svg" alt="license" />
</a>


Quick start
-------------
To quickly setup a working testing version of the backend, just use the command:
```[sh]
manage.py install
```
And then to run the server :
```[sh]
manage.py run-data-server
```



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
`manage.py install-deps`

Finally, initialize the database, and load static files
`manage.py init`

Usage
-----

The `manage.py` file provides some useful tools. Here is how to use it :

To start the data server, i.e. the one containing the database/django stuff
`manage.py run-data-server`

To start the notification server, i.e. the one which clients will open websockets to, use
`manage.py run-push-server`

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
