"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

import os
import sqlite3
from datetime import datetime

import pytz
from django.conf import settings

from .utils import (
    get_date_from_gps_time,
    dict_factory,
)


class Observation(object):
    """
    Class to define a single observation
    """

    def __init__(self, observation_id):
        """
        Initializing observation class from the observation id
        :param observation_id: number representing observation id
        """
        self.health_okay = True

        self.observation_id = observation_id
        self.processing_objects = []

        # creating the connection and cursor
        try:
            self.conn = sqlite3.connect(settings.GLEAM_DATABASE_PATH)

            self.conn.row_factory = dict_factory

            self.cursor = self.conn.cursor()

        except sqlite3.Error:
            self.health_okay = False

        # collecting information in groups for an observation.
        self.attributes, self.histogram_attributes = self._populate_observation_info()
        self.processing_objects = self._populate_processing_objects()
        self.carousel_amplitude, self.carousel_phase, self.histogram, self.phase_map = \
            self._populate_carousels_and_images()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.conn.close()
        except sqlite3.Error:
            pass

    def _populate_observation_info(self):
        """
        Populates observation attributes. These are used in template.
        :return: result and histogram attributes as dictionaries.
        """

        # query to collect observation attributes. Ordered in a way so that two column can have the required format.
        # For example: ra_pointing, dec_pointing are in the same column.
        query = 'SELECT ' \
                '{0}.obsname, ' \
                'cenchan || " (" || CAST(1.28 * {0}.cenchan AS INT) || " MHz)" cenchan, ' \
                '{0}.ra_pointing, ' \
                '{0}.delays, ' \
                '{0}.dec_pointing, ' \
                'CASE WHEN {0}.calibration = 0 THEN \'False\' ELSE \'True\' END calibration, ' \
                '{0}.azimuth_pointing, ' \
                '{0}.cal_obs_id, ' \
                '{0}.elevation_pointing, ' \
                '{0}.calibrators, ' \
                '{0}.peelsrcs, ' \
                '{0}.flags, ' \
                '{0}.selfcal, ' \
                '{0}.ion_phs_med, ' \
                '{0}.ion_phs_peak, ' \
                '{0}.ion_phs_std, ' \
                'CASE WHEN {0}.archived = 0 THEN \'False\' ELSE \'True\' END archived, ' \
                'obs_id "UTC date-obs", ' \
                '{0}.status ' \
                ' FROM {0} WHERE obs_id = ?'.format('observation')

        values = [self.observation_id]

        result = dict(self.cursor.execute(query, values).fetchone())

        # separating the histogram attributes as they are to be displayed near the histogram.
        histogram_attributes = dict(
            ion_phs_med=result.pop('ion_phs_med', None),
            ion_phs_peak=result.pop('ion_phs_peak', None),
            ion_phs_std=result.pop('ion_phs_std', None),
        )

        # converting gps time to UTC date
        result.update({
            "UTC date-obs": get_date_from_gps_time(result.get('UTC date-obs')),
        })

        return result, histogram_attributes

    def _populate_processing_objects(self):
        """
        Populate processing object information for the observation.
        :return: list of processing objects.
        """

        # query to extract processing information
        query = 'SELECT ' \
                '{0}.start_time, ' \
                '{0}.submission_time, ' \
                '{0}.task, ' \
                '{0}.job_id, ' \
                '{0}.task_id ,' \
                '{0}.user, ' \
                '{0}.status, ' \
                '{0}.stderr, ' \
                '{0}.stdout ' \
                ' FROM {0} WHERE obs_id = ? ORDER BY start_time DESC'.format('processing')

        values = [self.observation_id]

        results = self.cursor.execute(query, values).fetchall()

        processing_objects = []

        utc_tz = pytz.timezone('UTC')
        perth_tz = pytz.timezone('Australia/Perth')

        for result in results:
            processing_dict = dict(result)

            unix_time = result.get('submission_time')
            if unix_time:
                utc_time = utc_tz.localize(datetime.fromtimestamp(unix_time))
                awst_time = utc_time.astimezone(perth_tz)
                processing_dict.update({
                    'submission_time': awst_time.strftime('%d/%m/%Y %H:%M:%S (%Z)'),
                })

            unix_time = result.get('start_time')
            if unix_time:
                utc_time = utc_tz.localize(datetime.fromtimestamp(unix_time))
                awst_time = utc_time.astimezone(perth_tz)
                processing_dict.update({
                    'start_time': awst_time.strftime('%d/%m/%Y %H:%M:%S (%Z)'),
                })

            processing_objects.append(processing_dict)

        return processing_objects

    def _populate_carousels_and_images(self):
        """
        Collects the images for carousels (amplitude and phase), histogram and phase map.
        :return: lists of carousel images, histogram and phase map images.
        """
        carousel_amplitude = []
        carousel_phase = []
        histogram = None
        phase_map = None

        # constructing the path for image store for this observation
        image_path = os.path.join(settings.BASE_DIR, '..', 'static', 'images', 'plots', self.observation_id)

        files = []
        for (dir_path, dir_names, file_names) in os.walk(image_path):
            files.extend(file_names)

        files = sorted(files)

        # categorising each file based on the name suffix.
        for file_name in files:
            if file_name.endswith('_amp.png'):
                carousel_amplitude.append(os.path.join('images', 'plots', self.observation_id, file_name))
            elif file_name.endswith('_phase.png'):
                carousel_phase.append(os.path.join('images', 'plots', self.observation_id, file_name))
            elif file_name.endswith('_histogram.png'):
                histogram = os.path.join('images', 'plots', self.observation_id, file_name)
            elif file_name.endswith('_phasemap.png'):
                phase_map = os.path.join('images', 'plots', self.observation_id, file_name)

        return carousel_amplitude, carousel_phase, histogram, phase_map
