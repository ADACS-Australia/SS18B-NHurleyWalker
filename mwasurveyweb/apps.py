"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.apps import AppConfig

from django.conf import settings


class MwasurveywebConfig(AppConfig):
    name = 'mwasurveyweb'
    verbose_name = 'GLEAM-X Survey'

    def ready(self):
        import mwasurveyweb.signals

        if not settings.TESTING:

            try:
                # not generating the plots if they are already generated.
                from mwasurveyweb.models import SkyPlot
                from mwasurveyweb.utility.skyplots import generate_sky_plots

                if not SkyPlot.objects.exists():
                    generate_sky_plots()
            except:
                pass

