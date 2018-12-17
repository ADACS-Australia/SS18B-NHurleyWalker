"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.test import TestCase

from ..utility.skyplots import generate_sky_plots


class TestSkyPlotGeneration(TestCase):

    def test_sky_plot_generation(self):
        generate_sky_plots()
