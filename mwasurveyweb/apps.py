from django.apps import AppConfig


class MwasurveywebConfig(AppConfig):
    name = 'mwasurveyweb'
    verbose_name = 'GLEAM-X Survey'

    def ready(self):
        import mwasurveyweb.signals

        # not generating the plots if they are already generated.
        from mwasurveyweb.models import SkyPlot
        from mwasurveyweb.utility.skyplots import generate_sky_plots

        if not SkyPlot.objects.exists():
            generate_sky_plots()

