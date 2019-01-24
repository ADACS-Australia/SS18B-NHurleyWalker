"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

SITE_URL = 'http://127.0.0.1:8000'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_FROM = 'ssaleheen@swin.edu.au'
EMAIL_HOST = 'mail.swin.edu.au'
EMAIL_PORT = 25

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'mwasurvey',
#         'USER': 'root',
#         'PASSWORD': 'your password',
#     },
# }
#
# for logger in LOGGING['loggers']:
#     LOGGING['loggers'][logger]['handlers'] = ['console', 'file']

LOGOUT_REDIRECT_URL = '/accounts/login/'

try:
    from .local import *
except ImportError:
    pass
