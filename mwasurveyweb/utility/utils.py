"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

import sqlite3

from django.conf import settings
from datetime import datetime

from thirdparty import leapseconds

from ..constants import *
from ..models import SearchInput


def get_gps_time_from_date(date_string):
    """
    Finds the gps time from a date string. This uses a third-party library obtained from:
    https://gist.github.com/zed/92df922103ac9deb1a05#file-leapseconds-py
    which uses the system tzinfo for finding leapseconds.
    :param date_string: string representation of the date. Must be in the following formats:
        1.  %d/%m/%Y %H:%M:%S
        2.  %d/%m/%YT%H:%M:%S
        2.  %d/%m/%Y
    :return: string (of gps time) or None if format is ambiguous.
    """

    # creating datetime object from the string date
    try:
        datetime_object = datetime.strptime(date_string.replace('T', ' '), '%d/%m/%Y %H:%M:%S')
    except ValueError:
        try:
            datetime_object = datetime.strptime(date_string, '%d/%m/%Y')
        except ValueError:
            return None

    # calculating gps time (which is a datetime object) using the leapseconds library
    gps_time = leapseconds.utc_to_gps(datetime_object)

    # finding the time delta from the gps time epoch.
    delta = gps_time - datetime(1980, 1, 6)

    # returning the string of the delta in seconds
    return str(int(delta.total_seconds()))


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


def get_value_and_operators(value, search_input, search_form, input_properties):

    try:
        index = input_properties[2]
    except IndexError:
        index = None

    value_adjusted = None

    try:
        if search_input.field_type == SearchInput.INT:
            value_adjusted = int(value)
        elif search_input.field_type == SearchInput.FLOAT:
            value_adjusted = float(value)
        elif search_input.field_type == SearchInput.BOOL:
            value_adjusted = 1 if value else 0
        else:
            value_adjusted = value
    except (TypeError, ValueError):
        pass

    radius_value = 0  # for Non RADIUS inputs it does not matter

    # finding appropriate value for RADIUS input types
    if search_input.input_type == RADIUS:
        field_name = '__'.join(input_properties[:-1] + ['1' if input_properties[2] == '0' else '0'])

        radius_value = search_form['form'].cleaned_data.get(field_name) \
            if search_form['form'].cleaned_data.get(field_name) else 0

        if search_input.field_type == SearchInput.INT:
            radius_value_adjusted = int(radius_value)
        elif search_input.field_type == SearchInput.FLOAT:
            radius_value_adjusted = float(radius_value)
        else:
            radius_value_adjusted = radius_value

        value_adjusted += radius_value_adjusted * (-1 if input_properties[2] == '0' else 1)

    operator, field_operator = get_operator_by_input_type(search_input.input_type, index, second_value=radius_value)

    return value_adjusted, operator, field_operator


def get_operator_by_input_type(input_type, index=None, second_value=0):
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

    elif input_type == RADIUS:
        if index == '0':
            operator = '>=' if second_value else '='
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


def get_page_type(path_info):
    if 'search_' in path_info:
        return list(filter(None, path_info.split('/')))[0].replace('search_', '')
    elif 'view_' in path_info:
        return list(filter(None, path_info.split('/')))[0].replace('view_', '')


def get_search_results(query, query_values):

    try:

        conn = sqlite3.connect(settings.GLEAM_DATABASE_PATH)

        cursor = conn.cursor()

        # to handle subquery for total object count, values need to be duplicated in order
        values = query_values + query_values

        return cursor.execute(query, values).fetchall(),

    except sqlite3.Error:
        return [[]]
