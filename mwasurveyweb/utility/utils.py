"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

import sqlite3

from django.conf import settings

from ..constants import *


def check_forms_validity(search_forms):
    """
    Checks validity of search forms.
    :param search_forms: list of search forms
    :return: True if all forms are valid, otherwise False
    """

    for search_form in search_forms:

        if not search_form.get('form').is_valid():
            return False

    return True


def get_operator_by_field_type(field_type, index=None):
    if field_type == TEXT:
        return 'LIKE'

    if field_type == NUMBER:
        return '='

    if field_type == RANGE:
        if index == '0':
            return '>='
        if index == '1':
            return '<='


def get_search_results(query, query_values):

    try:

        conn = sqlite3.connect(settings.GLEAM_DATABASE_PATH)

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        # to handle subquery for total object count, values need to be duplicated in order
        values = query_values + query_values

        return cursor.execute(query, values).fetchall(),

    except sqlite3.Error:
        return []
