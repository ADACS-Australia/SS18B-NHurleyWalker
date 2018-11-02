"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.db import migrations

from mwasurveyweb.constants import *


def insert(apps, schema_editor):
    SearchInputGroup = apps.get_model('mwasurveyweb', 'SearchInputGroup')

    SearchInput = apps.get_model('mwasurveyweb', 'SearchInput')

    # inserting the fields for Observation Info Constraints
    try:
        info_group = SearchInputGroup.objects.get(name='observation_info')

    except SearchInputGroup.DoesNotExist:
        pass

    else:

        initial_search_input_info = [
            ('project_id', 'Project ID', 'observation', 'projectid', TEXT, None, None, False, 0, ''),
            ('observation_name', 'Observation Name', 'observation', 'obsname', TEXT, None, None, False, 1, ''),
            ('creator', 'Creator', 'observation', 'creator', TEXT, None, None, False, 2, ''),
            ('calibration', 'Calibration', 'observation', 'calibration', CHECKBOX, None, None, False, 3,
             'Check to find observations flagged as calibrators.'),
        ]

        for search_input_info in initial_search_input_info:
            SearchInput.objects.create(
                search_input_group=info_group,
                name=search_input_info[0],
                display_name=search_input_info[1],
                table_name=search_input_info[2],
                field_name=search_input_info[3],
                field_type=search_input_info[4],
                initial_value=search_input_info[5],
                placeholder=search_input_info[6],
                required=search_input_info[7],
                display_order=search_input_info[8],
                input_info=search_input_info[9],
            )

    # inserting the fields for Pointing Constraints
    try:
        info_group = SearchInputGroup.objects.get(name='pointing')

    except SearchInputGroup.DoesNotExist:
        pass

    else:

        initial_search_input_info = [
            ('ra', 'RA in deg', 'observation', 'ra_pointing', RANGE, None, None, False, 0, ''),
            ('dec', 'Dec in deg', 'observation', 'dec_pointing', RANGE, None, None, False, 1, ''),
            ('elevation', 'Elevation in deg', 'observation', 'elevation_pointing', RANGE, None, None, False, 2, ''),
            ('azimuth', 'Azimuth in deg', 'observation', 'azimuth_pointing', RANGE, None, None, False, 3, ''),
            ('gridpoint_number', 'Gridpoint number', 'observation', 'azimuth_pointing', RANGE, None, None, False, 4,
             ''),
        ]

        for search_input_info in initial_search_input_info:
            SearchInput.objects.create(
                search_input_group=info_group,
                name=search_input_info[0],
                display_name=search_input_info[1],
                table_name=search_input_info[2],
                field_name=search_input_info[3],
                field_type=search_input_info[4],
                initial_value=search_input_info[5],
                placeholder=search_input_info[6],
                required=search_input_info[7],
                display_order=search_input_info[8],
                input_info=search_input_info[9],
            )

    # inserting the fields for Time Constraints
    try:
        info_group = SearchInputGroup.objects.get(name='time')

    except SearchInputGroup.DoesNotExist:
        pass

    else:

        initial_search_input_info = [
            ('start_time_gps', 'Starttime in GPS seconds', 'observation', 'starttime', RANGE, None, None, False, 0, ''),
            # missing one here
            ('obs_duration', 'Obs duration, in seconds', 'observation', 'duration_sec', RANGE, None, None, False, 2,
             ''),
            ('future', 'Future', 'observation', 'starttime', CHECKBOX, None, None, False, 3,
             'Check to find observations in the future, rather than the past.'),
        ]

        for search_input_info in initial_search_input_info:
            SearchInput.objects.create(
                search_input_group=info_group,
                name=search_input_info[0],
                display_name=search_input_info[1],
                table_name=search_input_info[2],
                field_name=search_input_info[3],
                field_type=search_input_info[4],
                initial_value=search_input_info[5],
                placeholder=search_input_info[6],
                required=search_input_info[7],
                display_order=search_input_info[8],
                input_info=search_input_info[9],
            )


def revert(apps, schema_editor):
    SearchInput = apps.get_model('mwasurveyweb', 'SearchInput')

    SearchInput.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('mwasurveyweb', '0002_insert_input_groups'),
    ]

    operations = [
        migrations.RunPython(code=insert, reverse_code=revert)
    ]
