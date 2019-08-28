"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

import os
import itertools
import sqlite3
import astropy.units as u
import logging

from astropy.coordinates import SkyCoord

from django.conf import settings
from django.utils import timezone

from ..models import (
    SkyPlotsConfiguration,
    Colour,
    SkyPlot,
)

import matplotlib

# this must be used like the following
# setting up the matplotlib backend as 'Agg'
matplotlib.use('Agg')
# now importing the pyplot
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def generate_sky_plot_by_colour(colour_set, cursor, is_default=False):
    """
    This function generates a sky plot by colours. A colour can resemble more than one status and hence, for each colour
    this function finds the related observations and plots them in the graph using the associated colour code.
    :param colour_set: set of colour
    :param cursor: cursor to execute queries to the GLEAM-X database
    :param is_default: boolean to indicate whether this plot is the default to show on the landing page
    :return: nothing, but saves an image
    """

    # query to retrieve ra and dec for observation
    query = 'SELECT ra_pointing, dec_pointing FROM observation WHERE status = ?'

    # figure/plot configuration
    plt.figure(figsize=(16, 8.4))
    plt.subplot(111, projection="aitoff")
    plt.grid(True)

    # list to store distinct colour names
    colours = []

    for colour in colour_set:

        # finding the related status for a colour
        status_list = SkyPlotsConfiguration.objects.filter(colour=colour).values('observation_status')

        for status in status_list:

            # finding the observations' information for the status
            results = cursor.execute(query, [status.get('observation_status')]).fetchall()
            ra = []
            dec = []

            # creating list of ra and dec
            for row in results:
                ra.append(row[0])
                dec.append(row[1])

            # continue to the next status if there are no observations found for the current status
            if not len(ra):
                continue

            # Otherwise, change to sky-coordinates and find ra and dec in radian
            c = SkyCoord(ra=ra, dec=dec, frame='icrs', unit=(u.degree, u.degree))
            ra_rad = c.ra.wrap_at(180 * u.deg).radian
            dec_rad = c.dec.radian

            # plot ra and dec in the graph
            plt.plot(ra_rad, dec_rad, 'o', markersize=40, alpha=0.1, color='#{}'.format(colour.code))

        colours.append(colour.name)

    # constructing the image name
    image_name = '_'.join(colours)

    # for no colour image, the name must be blank
    if not image_name:
        image_name = 'blank'

    # construct the image path to save the image
    file_path = os.path.join(
        settings.BASE_DIR,
        '..',
        'static/images/skyplots/',
        '{}.png'.format(image_name),
    )

    # save the image in the physical location
    plt.savefig(file_path)
    plt.close()

    # create or update an entry to the database, so that it is available
    SkyPlot.objects.update_or_create(
        name='/images/skyplots/{}.png'.format(image_name),
        defaults={
            "generation_time": timezone.localtime(timezone.now()),
            "is_default": is_default,
        }
    )


def generate_sky_plots():
    """
    Generates sky plots based on the information stored in the GLEAM-X database and application's default database.
    """

    # finding the current time.
    now = timezone.localtime(timezone.now())

    # connect to gleam-x database
    try:

        conn = sqlite3.connect(settings.GLEAM_DATABASE_PATH)

        cursor = conn.cursor()

    except sqlite3.Error as ex:
        print('Could not generate plots due to SQLite error : ' + ex.__str__())
        logger.info('Could not generate plots due to SQLite error : ' + ex.__str__())
    else:

        # find out the colours, in order, so that names would be consistent
        colours = Colour.objects.all().order_by('name')

        # for each combination of colour, a sky plot is generated
        for L in range(0, len(colours) + 1):
            for subset in itertools.combinations(colours, L):
                generate_sky_plot_by_colour(subset, cursor, is_default=(L == len(colours)))

        try:
            conn.close()
        except sqlite3.Error:
            pass

    # clean up the image files
    SkyPlot.objects.filter(generation_time__lt=now).delete()
