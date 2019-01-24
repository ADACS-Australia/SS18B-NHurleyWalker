"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from .development import *

TESTING = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

TEST_OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'test_output')

LOGGING['loggers']['django']['handlers'] = ['file']
LOGGING['loggers']['mwasurveyweb']['handlers'] = ['file']
