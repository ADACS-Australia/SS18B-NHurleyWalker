"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

import sqlite3

from django.conf import settings


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Processing(object):
    def __init__(self, processing_id):
        self.health_okay = True

        self.processing_id = processing_id
        self.observation = None

        # creating the connection and cursor
        try:
            self.conn = sqlite3.connect(settings.GLEAM_DATABASE_PATH)

            self.conn.row_factory = dict_factory

            self.cursor = self.conn.cursor()

        except sqlite3.Error:
            self.health_okay = False

        self.attributes, self.observation_attributes = self._populate_processing_info()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.conn.close()
        except sqlite3.Error:
            pass

    def _populate_processing_info(self):

        query = 'SELECT ' \
                '{0}.job_id, ' \
                '{0}.submission_time, ' \
                '{0}.start_time, ' \
                '{0}.end_time, ' \
                '{0}.task_id, ' \
                '{0}.task, ' \
                '{0}.user, ' \
                '{0}.obs_id, ' \
                '{0}.batch_file, ' \
                '{0}.stderr, ' \
                '{0}.stdout, ' \
                '{0}.output_files, ' \
                '{0}.status ' \
                ' FROM {0} WHERE job_id = ?'.format('processing')

        values = [self.processing_id]

        result = dict(self.cursor.execute(query, values).fetchone())

        observation_attributes = dict(
            obs_id=result.pop('obs_id', None),
        )

        return result, observation_attributes
