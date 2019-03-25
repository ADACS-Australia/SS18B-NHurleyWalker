"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

import sqlite3
import pytz

from django.conf import settings
from datetime import datetime, date, time, timedelta

from thirdparty import leapseconds

from .. import constants


def dict_factory(cursor, row):
    """
    Factory function to convert a sqlite3 result row in a dictionary
    :param cursor: cursor object
    :param row: a row object
    :return: dictionary representation of the row object
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_order_by_parts(order_by):
    """
    Extract the order by clause information. In future this could be used to update multiple column ordering.
    :param order_by: the order by clause, for example: ' ORDER BY column_name ASC/DESC'
    :return: order by field name, order by order. For example: column_name, ASC/DESC
    """
    order_by_parts = order_by.replace(' ORDER BY ', '').strip().split()

    return order_by_parts[0], order_by_parts[1]


def update_display_headers_order_by(display_headers, order_by):
    """
    Updates the current display headers according to the order by clause of the query. This is used to display
    appropriate icon in the UI.

    :param display_headers: A list of display headers where an item in the list is in the following format:
    dict(
        display=table_column.display_name, # this is the display text which will appear in the UI as a column header
        field_name=table_column.field_name, # name of field used for creating the sort link, ex: ?sort=field_name
        sort_order='', # the current sort order of the column, possible values:
            '' --> No sort
            '-up' --> ASC sort
            '-down' --> DESC sort
    )
    :param order_by: String that defines the ORDER BY of the query. Format:
    ' ORDER BY column_name ASC/DESC'
    :return: updated display_headers with appropriate order by direction
    """

    order_by_field, oder_by_direction = get_order_by_parts(order_by)

    for display_header in display_headers:

        # default sort order
        sort_order = ''

        if display_header.get('field_name') == order_by_field:
            # this field needs to be updated by order by
            sort_order = '-up' if oder_by_direction == 'ASC' else '-down'

        # update the display header
        display_header.update({
            'sort_order': sort_order,
        })

    return display_headers


def get_unix_time_from_date(date_object):
    """
    Finds the unix timestamp from a date string
    :param date_object: datetime object
    :return: string (of unix timestamp)
    """

    # converting date object to datetime object
    if type(date_object) == date:
        datetime_utc_object = datetime(
            year=date_object.year,
            month=date_object.month,
            day=date_object.day,
            tzinfo=pytz.utc,
        )

        return datetime_utc_object.timestamp()

    return None


def get_gps_time_from_date(datetime_object):
    """
    Finds the gps time from a date string. This uses a third-party library obtained from:
    https://gist.github.com/zed/92df922103ac9deb1a05#file-leapseconds-py
    which uses the system tzinfo for finding leapseconds.
    :param datetime_object: datetime object
    :return: string (of gps time)
    """

    # converting date object to datetime object
    if type(datetime_object) == date:
        datetime_object = datetime.combine(datetime_object, time=time())

    # calculating gps time (which is a datetime object) using the leapseconds library
    gps_time = leapseconds.utc_to_gps(datetime_object)

    # finding the time delta from the gps time epoch.
    delta = gps_time - datetime(1980, 1, 6)

    # returning the string of the delta in seconds
    return str(int(delta.total_seconds()))


def get_date_from_gps_time(gps_time):
    """
    Finds the date from a gps time. This uses a third-party library obtained from:
    https://gist.github.com/zed/92df922103ac9deb1a05#file-leapseconds-py
    which uses the system tzinfo for finding leapseconds.
    :param gps_time: gps time text/integer
    :return: date_object: date time object
    """

    # converting date object to datetime object
    if type(gps_time) != int:
        try:
            gps_time = int(gps_time)
        except (ValueError, TypeError, AttributeError):
            return None

    # calculating date (which is a datetime object) using the leapseconds library
    date_object = leapseconds.gps_to_utc(datetime(1980, 1, 6) + timedelta(seconds=gps_time))

    # returning the date object
    return date_object


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


def get_operator_by_input_type(input_type, index=None, second_value=0):
    """
    calculate operator and field operator for an input type. Given: a query clause count(a.b) > c
        'count' is the field_operator
        '>' is the operator
    Based on the input type the operator and field operator are determined.
    :param input_type: string determining the type of input.
    :param index: integer defining the index of the input for multiple inputs.
    :param second_value: value on which the operator may be dependent. For multiple inputs second value determines the
    operator.
    :return: operator and field operator string
    """
    operator = None
    field_operator = None

    if input_type == constants.TEXT:
        operator = 'LIKE'

    elif input_type == constants.NUMBER:
        operator = '='

    elif input_type == constants.RANGE:
        if index == '0':
            operator = '>='
        if index == '1':
            operator = '<='

    elif input_type == constants.RADIUS:
        if index == '0':
            operator = '>=' if second_value else '='
        if index == '1':
            operator = '<='

    elif input_type == constants.MIN_NUMBER:
        operator = '>='

    elif input_type == constants.MAX_NUMBER:
        operator = '<='

    elif input_type == constants.MAX_ABSOLUTE_NUMBER:
        operator = '<='
        field_operator = 'ABS'

    elif input_type in [constants.DATE_GPS, constants.DATE_UNIX, ]:
        if index == '0':
            operator = '>='
        if index == '1':
            operator = '<='

    elif input_type in [constants.DATE_GPS_RANGE, constants.DATE_UNIX_RANGE, ]:
        if index == '0':
            operator = '>='
        if index == '1':
            operator = '<='

    elif input_type == constants.SELECT:
        operator = '='

    elif input_type == constants.CHECKBOX:
        operator = '='

    return operator, field_operator


def get_page_type(path_info):
    """
    Returns the page type from the django path information
    :param path_info: string - django path information
    :return: string defining the type of page. For example: 'observation' or 'processing'
    """
    if 'search_' in path_info:
        return list(filter(None, path_info.replace(settings.ROOT_SUBDIRECTORY_PATH, '').split('/')))[0]\
            .replace('search_', '')
    elif 'view_' in path_info:
        return list(filter(None, path_info.replace(settings.ROOT_SUBDIRECTORY_PATH, '').split('/')))[0]\
            .replace('view_', '')


def get_search_results(query, query_values):
    """
    Performs the query and returns the search result.
    :param query: The query string
    :param query_values: list of query values to replace the ?s in the query string
    :return: list of search result
    """
    try:

        conn = sqlite3.connect(settings.GLEAM_DATABASE_PATH)

        cursor = conn.cursor()

        # to handle subquery for total object count, values need to be duplicated in order
        values = query_values + query_values

        results = cursor.execute(query, values).fetchall(),

    except sqlite3.Error:
        return [[]]
    else:

        try:
            conn.close()
        except sqlite3.Error:
            pass

        return results
