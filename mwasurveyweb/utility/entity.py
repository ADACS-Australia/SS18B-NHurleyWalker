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


class Entity(object):

    def __init__(self, object_type, object_id):
        self.health_okay = True

        self.object_type = object_type
        self.object_id = object_id
        self.related_entities = []

        # creating the connection and cursor
        try:
            conn = sqlite3.connect(settings.GLEAM_DATABASE_PATH)

            conn.row_factory = dict_factory

            self.cursor = conn.cursor()

        except sqlite3.Error:
            self.health_okay = False

        self.entity_attributes = self._populate_object_info()
        self.related_entities = self._populate_related_entities()
        self.carousel_amplitude, self.carousel_phase = self._populate_carousels()

    def _populate_object_info(self):

        query = 'SELECT * FROM {} WHERE obs_id = ?'.format(self.object_type)

        values = [self.object_id]

        result = dict(self.cursor.execute(query, values).fetchone())

        return result

    def _populate_related_entities(self):
        return dict()

    def _populate_carousels(self):
        carousel_amplitude = []
        carousel_phase = []

        image_path = os.path.join(settings.BASE_DIR, '..', 'static', 'images', 'plots', self.object_id)

        files = []
        for (dir_path, dir_names, file_names) in os.walk(image_path):
            files.extend(file_names)

        files = sorted(files)

        for file_name in files:
            if file_name.endswith('_amp.png'):
                carousel_amplitude.append(os.path.join('images', 'plots', self.object_id, file_name))
            elif file_name.endswith('_phase.png'):
                carousel_phase.append(os.path.join('images', 'plots', self.object_id, file_name))

        return carousel_amplitude, carousel_phase
