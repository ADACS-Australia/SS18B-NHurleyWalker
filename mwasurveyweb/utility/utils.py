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


def get_operator_by_input_type(input_type, index=None):
    operator = None
    field_operator = None

    if input_type == TEXT:
        operator = 'LIKE'

    elif input_type == NUMBER:
        operator = '='

    elif input_type == RANGE:
        if index == '0':
            operator = '>='
        if index == '1':
            operator = '<='

    elif input_type == MIN_NUMBER:
        operator = '>='

    elif input_type == MAX_NUMBER:
        operator = '<='

    elif input_type == MAX_ABSOLUTE_NUMBER:
        operator = '<='
        field_operator = 'ABS'

    elif input_type == SELECT:
        operator = '='

    elif input_type == CHECKBOX:
        operator = '='

    return operator, field_operator


def get_search_page_type(path_info):
    return path_info.replace('/', '').replace('search_', '')


def get_search_results(query, query_values):

    try:

        conn = sqlite3.connect(settings.GLEAM_DATABASE_PATH)

        cursor = conn.cursor()

        # to handle subquery for total object count, values need to be duplicated in order
        values = query_values + query_values

        return cursor.execute(query, values).fetchall(),

    except sqlite3.Error:
        return [[]]
