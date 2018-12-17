from django.apps import AppConfig
from django.conf import settings


class MwasurveywebConfig(AppConfig):
    name = 'mwasurveyweb'
    verbose_name = 'GLEAM-X Survey'

    def ready(self):

        # not generating the plots if it is a development server.
        if not settings.DEBUG:
            print('bingo...')
        pass
