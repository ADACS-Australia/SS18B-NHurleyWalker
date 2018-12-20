"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.shortcuts import render

from ..models import (
    SkyPlotsConfiguration,
    SkyPlot,
)


def index(request):
    """
    Render the index view.
    :param request: Django request object.
    :return: Rendered template
    """

    sky_plots = SkyPlot.objects.all()

    return render(
        request,
        "mwasurveyweb/welcome.html",
        {
            'sky_plots': sky_plots,
        }
    )


def about(request):
    """
    Render the about view.
    :param request: Django request object.
    :return: Rendered template
    """
    return render(
        request,
        'mwasurveyweb/about.html',
    )


def error_404_view(request, exception):
    """
    Render custom 404 page.
    :param request: Django request object.
    :return: Rendered template
    """
    data = {"name": "not used yet"}
    return render(request, 'mwasurveyweb/error_404.html', data)
