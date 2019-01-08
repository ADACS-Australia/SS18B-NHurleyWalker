"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.core.management import BaseCommand

from ...utility.skyplots import generate_sky_plots


class Command(BaseCommand):
    """
    Django management command class to update skyplots when configuration changes occur.
    """

    help = 'Generates sky plots based on the current configuration and removes any obsolete ones before finishes'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        generate_sky_plots()
