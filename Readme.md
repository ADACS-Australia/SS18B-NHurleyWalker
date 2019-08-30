Project Overview
================

This project serves as a user-interface for searching the GLEAM-X Survey. The UI is responsible for controlling
and managing user input, retrieving and representing information.

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
* `git clone ...` (clone the code)
* `source venv/bin/activate` (activate the virtual environment)
* `cd SS18B-NHurleyWalker/mwasurvey/settings` (enter the settings directory)
* `touch local.py` (create the file for local settings - refer to the Local Settings section for setting up a local settings file)
* `cd ../../` (enter the root directory of the project)
* `mv/cp ... GLEAM-X.sqlite` (copy the GLEAM-X database, if you copy it to another folder you need to update it in the local settings. See local settings for details. Path should be matched)
* `pip3 install -r requirements.txt` (install required python packages)
* `./(development-)manage.py migrate` (migrate - this will set up initial search parameters and sky-plot configuration)
* `./(development-)manage.py createsuperuser` (create an admin account) (specify the required manage.py file instead)
* `./(development-)manage.py runserver 8000` (running the server)

## Local Settings ##

The project is required to have customised machine specific settings. Those settings need to be included or overridden 
in the local settings file. Create one local.py in the settings module next to the other settings files (`base.py`, 
`development.py`, `production.py` etc.)

```python
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

The following settings needs to be present in the `local.py` settings file.

* The secret key used to authenticate the workflow with the UI API (can be generated with e.g. https://www.miniwebtool.com/django-secret-key-generator/)
```python
SECRET_KEY = 'some really long string with $YMb0l$'
```

* Some other settings required for running the app under a sub-directory:
```python
# Configure it for production if required
ROOT_SUBDIRECTORY_PATH = ''

# Configure it for production if required
SITE_URL = ''

# Only to be true when testing, eg: from test settings
TESTING = False
```
* GLEAM-X database path. Should be matched while copying the database file in configuration step above.
```python
# Update it if you have a different name or want to store the database in some other directory.
GLEAM_DATABASE_PATH = os.path.join(BASE_DIR, '..', 'GLEAM-X.sqlite')
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
Alternatively SQL-Lite database settings could be:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../mwasurvey.sqlite3'),
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

## Management Commands ##

* ```./development-manage.py update_user_input_options``` (This will read the Gleam-X database, as provided in the 
settings file and update the Users (SELECT input) options by finding distinct users from the `processing` table).
Each time the GLEAM-X database is updated, this command should be run to keep the user list up to date.

* ```./development-manage.py update_skyplots``` (This will update the skyplots that are shown in the landing page.
This is required if you are changing skyplots configuration. Note: During startup, the skyplots configurations will
be checked and skyplots will be generated if required. In this case, startup may take some additional time.

## SITE ADMINISTRATION ##

Once running, `/admin` would take you to the django admin where you can control the UI inputs, search pages and few 
other things. Following will give a description of how things should be changed.

### Sky Plots ###

Sky plots that are generated are stored in the `Sky plots` model. The default one is the one which is shown when the 
welcome/landing page is loaded. Entries on this table are auto-generated or should be generated by management command
if required. Manually changing these is discouraged.

Sky plot configuration is done in two models. `Colour` model keep colour names and colour codes, which are then used in
rendering the plot points and displaying the texts (besides the buttons) in the landing page. `Sky plot configuration`
has entries which hold observation status names (should be matched with the gleam-x database) and corresponding colour
information.

### Search ###

* `Search Page` model defines the number of search pages and their names. This contributes the search menu as well.
* `Search Input Group` are small forms that appear in the search page (in the UI). It has a name, which has a prefix of 
the search page it belongs to. Display name is the text that is used the form header in the UI. Any description would 
show up in the UI as well as a note. 
* `Search Page Input Group` model stores the input groups that will be displayed in the search page.
* `Search Input` model defines the inputs that would show up in the search forms. Each input is associated with an input
group and has a name and display name. `Table name`, `Field name` and `Field Type` are the actual table and field name 
as per GLEAM-X database. `Input Type` defines how the input would be rendered in the UI. `Initial value` and `Placeholder`
are default value and placeholder respectively. If `Required` is checked, this input must have been inputted by the user.
Importantly, `Display order` defines in which order the input will be shown in the form snippets on the UI. 
* `Search Input Option` model stores the option values for `select`, `radio` inputs. Each search input belongs to a
search input and has an order by which it will appear in the UI.

### Search Result Page ###

`Search Page Display Colum` model defines the columns that are shown in the search result page. Each entry in this model 
belongs to a search page and also refers to a specific column in the database (defined by `Table name` and `Field name`).
Display name is the column header in the UI and display order is the order by which columns are displayed. Entering 
anything that is not in the GLEAM-X database would result in an invalid query and hence 0 results would be fetched.


## License ##

The project is licensed under the MIT License. For more information, please refer to the `LICENSE` included in
the root of the project.


## Authors ##
* [Shibli Saleheen](https://github.com/shiblisaleheen) (as part of [ADACS](https://adacs.org.au/))
* [Lewis Lakerink](https://github.com/retsimx) (as part of [ADACS](https://adacs.org.au/))
