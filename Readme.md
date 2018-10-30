Project Overview
================

This project serves as a user-interface and job controller for the MWA Survey. The UI is responsible for controlling
and managing user input, retrieve and represent information.

Prerequisites
=============
* Python 3.6+
* MySQL 5.7+ (tested with 5.7)

Optional

* Docker and Docker-Compose (If you want to use skip manual setup steps and just want to run the UI as a
docker container)

# Setup #

You might need to install `python-dev`, `python3-dev` and `libmysqlclient-dev` using the following
commands:

```shell
sudo apt-get install python-dev python3-dev
sudo apt-get install libmysqlclient-dev
```

beforehand for successful completion of the command:

```shell
pip install -r requirements.txt
```

## Configuration Steps ##

The required steps include the following:

* `virtualenv -p python3.6 venv` (create the virtual environment, e.g. with https://docs.python.org/3/library/venv.html or https://github.com/pyenv/pyenv)
* `git pull` (clone the code)
* `source venv/bin/activate` (activate the virtual environment)
* `cd ADACS-SS18B-NHurleyWalker/mwasurvey/settings` (enter the settings directory)
* `touch local.py` (create the file for local settings - refer to the Local Settings section for setting up a local settings file)
* `cd ../../` (enter the root directory of the project)
* `pip3 install -r requirements.txt` (install required python packages)
* `./development-manage.py migrate` (migrate, for staging or production)
* `./development-manage.py createsuperuser` (create an admin account) (specify the required manage.py file instead)
* `./development-manage.py runserver 8000` (running the server)

## Local Settings ##

The project is required to have customised machine specific settings. Those settings need to be included or overridden 
in the local settings file. Create one local.py in the settings module next to the other settings files (`base.py`, 
`development.py`, `production.py` etc.)

The following settings needs to be present in the `local.py` settings file.

* The secret key used to authenticate the workflow with the UI API (can be generated with e.g. https://www.miniwebtool.com/django-secret-key-generator/)
```python
SECRET_KEY = 'some really long string with $YMb0l$'
```

* The admins of the site who will receive error emails.
```python
ADMINS = [
    ('Your Name', 'youremail@dd.ress'),
]

MANAGERS = ADMINS
```
* The address from where the server emails will be sent.
```python
SERVER_EMAIL = 'serveremail@dd.ress'
```

* The address from where the notification emails will be sent.

```python
EMAIL_FROM = 'mail@dd.ress'
```

* Other email settings can also be provided.
```python
EMAIL_HOST = 'gpo.dd.res'
EMAIL_PORT = 25
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
```

* Database settings. For example, a simple MySQL database can be configured using
```python
DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'mwasurvey',
    'USER': 'django',
    'PASSWORD': 'test-password#1',
    'HOST': 'localhost',
    'PORT': 3306,
    }
}
```

### Database Settings for Docker ###

To run using docker and MySQL, modify the `local.py` configuration file. 
Instead of using the database settings described above, use something in 
the lines of the following:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mwasurvey',
        'HOST': 'db',
        'USER': 'django',
        'PORT': 3306,
        'PASSWORD': 'test-docker_#1',
    },
}
```

The USER and PASSWORD should be in accordance with the information provided in the file `docker-compose.yml` 
included at the root of the project repository.


## License ##

The project is licensed under the MIT License. For more information, please refer to the `LICENSE` included in
the root of the project.


## Authors ##
* [Shibli Saleheen](https://github.com/shiblisaleheen) (as part of [ADACS](https://adacs.org.au/))
* [Lewis Lakerink](https://github.com/retsimx) (as part of [ADACS](https://adacs.org.au/))
