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

from ..models import SkyPlotsConfiguration, Colour

import matplotlib

# this must be used like the following
# setting up the matplotlib backend as 'Agg'
matplotlib.use('Agg')
# now importing the pyplot
import matplotlib.pyplot as plt


logger = logging.getLogger(__name__)


def generate_sky_plot_by_colour(colour_set, cursor):
    query = 'SELECT ra_pointing, dec_pointing FROM observation WHERE status = ?'

    # figure/plot configuration
    plt.figure(figsize=(16, 8.4))
    plt.subplot(111, projection="aitoff")
    plt.grid(True)

    colours = []

    for colour in colour_set:
        status_list = SkyPlotsConfiguration.objects.filter(colour=colour).values('observation_status')

        for status in status_list:
            results = cursor.execute(query, [status.get('observation_status')]).fetchall()
            ra = []
            dec = []

            for row in results:
                ra.append(row[0])
                dec.append(row[1])

            if not len(ra):
                continue

            c = SkyCoord(ra=ra, dec=dec, frame='icrs', unit=(u.degree, u.degree))
            ra_rad = c.ra.wrap_at(180 * u.deg).radian
            dec_rad = c.dec.radian

            plt.plot(ra_rad, dec_rad, 'o', markersize=3, alpha=1, color='#{}'.format(colour.code))

        colours.append(colour.name)

    image_name = '_'.join(colours)

    if not image_name:
        image_name = 'blank'

    file_path = os.path.join(
            settings.BASE_DIR,
            '..',
            'static/images/skyplots/',
            '{}.png'.format(image_name),
        )

    plt.savefig(file_path)
    plt.close()


def generate_sky_plots():
    # connect to gleam-x database
    try:

        conn = sqlite3.connect(settings.GLEAM_DATABASE_PATH)

        cursor = conn.cursor()

    except sqlite3.Error as ex:
        print('Could not generate plots due to SQLite error : ' + ex.__str__())
        logger.info('Could not generate plots due to SQLite error : ' + ex.__str__())
    else:
        colours = Colour.objects.all().order_by('name')

        for L in range(0, len(colours) + 1):
            for subset in itertools.combinations(colours, L):
                generate_sky_plot_by_colour(subset, cursor)
