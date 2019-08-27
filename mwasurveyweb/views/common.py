"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""
import time

from django.shortcuts import render

from ..models import (
    Colour,
    SkyPlotsConfiguration,
    SkyPlot,
)


def index(request):
    """
    Render the index view.
    :param request: Django request object.
    :return: Rendered template
    """

    # finding the sky plots
    sky_plots = SkyPlot.objects.all()

    # finding the colours, this is to render the text according to the sky plot colours
    colours = Colour.objects.all()

    # buttons to be rendered in the UI
    buttons = []

    for colour in colours:
        labels = []

        # gettting the skyplot configurations for the colour
        sky_plot_configurations = SkyPlotsConfiguration.objects.filter(colour=colour)

        # generating button labels for the sky plot configuration
        for sky_plot_configuration in sky_plot_configurations:
            labels.append(sky_plot_configuration.observation_status.capitalize())

        # listing the buttons
        buttons.append(
            dict(
                colour=colour,
                name='status_{}'.format(colour.name),
                display_text=', '.join(labels),
            )
        )

    now = int(time.time())

    return render(
        request,
        "mwasurveyweb/welcome.html",
        {
            'sky_plots': sky_plots,
            'buttons': buttons,
            'now': now
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
