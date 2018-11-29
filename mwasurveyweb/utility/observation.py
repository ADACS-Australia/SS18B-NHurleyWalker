"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

import os
import sqlite3

from django.conf import settings


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Observation(object):

    def __init__(self, observation_id):
        self.health_okay = True

        self.observation_id = observation_id
        self.processing_objects = []

        # creating the connection and cursor
        try:
            conn = sqlite3.connect(settings.GLEAM_DATABASE_PATH)

            conn.row_factory = dict_factory

            self.cursor = conn.cursor()

        except sqlite3.Error:
            self.health_okay = False

        self.attributes = self._populate_observation_info()
        self.processing_objects = self._populate_processing_objects()
        self.carousel_amplitude, self.carousel_phase = self._populate_carousels()

    def _populate_observation_info(self):

        query = 'SELECT ' \
                '{0}.obsname, ' \
                '{0}.ra_pointing, ' \
                '{0}.dec_pointing, ' \
                '{0}.azimuth_pointing, ' \
                '{0}.elevation_pointing, ' \
                'CAST(1.28 * {0}.cenchan AS INT) || " MHz" cenchan, ' \
                '{0}.delays, ' \
                '{0}.calibration, ' \
                '{0}.cal_obs_id, ' \
                '{0}.calibrators, ' \
                '{0}.peelsrcs, ' \
                '{0}.flags, ' \
                '{0}.selfcal, ' \
                '{0}.ion_phs_med, ' \
                '{0}.ion_phs_peak, ' \
                '{0}.ion_phs_std, ' \
                '{0}.archived, ' \
                '{0}.nfiles, ' \
                '{0}.status ' \
                ' FROM {0} WHERE obs_id = ?'.format('observation')

        values = [self.observation_id]

        result = dict(self.cursor.execute(query, values).fetchone())

        return result

    def _populate_processing_objects(self):

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

        for result in results:
            processing_objects.append(dict(result))

        return processing_objects

    def _populate_carousels(self):
        carousel_amplitude = []
        carousel_phase = []

        image_path = os.path.join(settings.BASE_DIR, '..', 'static', 'images', 'plots', self.observation_id)

        files = []
        for (dir_path, dir_names, file_names) in os.walk(image_path):
            files.extend(file_names)

        files = sorted(files)

        for file_name in files:
            if file_name.endswith('_amp.png'):
                carousel_amplitude.append(os.path.join('images', 'plots', self.observation_id, file_name))
            elif file_name.endswith('_phase.png'):
                carousel_phase.append(os.path.join('images', 'plots', self.observation_id, file_name))

        return carousel_amplitude, carousel_phase
