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
        info_group = SearchInputGroup.objects.get(name='Observation Info Constraints')

    except SearchInputGroup.DoesNotExist:
        pass

    else:

        initial_search_input_info = [
            ('Project ID', 'observation', 'projectid', TEXT, None, None, False, 0, ''),
            ('Observation Name', 'observation', 'obsname', TEXT, None, None, False, 1, ''),
            ('Creator', 'observation', 'creator', TEXT, None, None, False, 2, ''),
            ('Calibration', 'observation', 'calibration', CHECKBOX, None, None, False, 3,
             'Check to find observations flagged as calibrators.'),
        ]

        for search_input_info in initial_search_input_info:
            SearchInput.objects.create(
                search_input_group=info_group,
                display_name=search_input_info[0],
                table_name=search_input_info[1],
                field_name=search_input_info[2],
                field_type=search_input_info[3],
                initial_value=search_input_info[4],
                placeholder=search_input_info[5],
                required=search_input_info[6],
                display_order=search_input_info[7],
                input_info=search_input_info[8],
            )

    # inserting the fields for Pointing Constraints
    try:
        info_group = SearchInputGroup.objects.get(name='Pointing Constraints')

    except SearchInputGroup.DoesNotExist:
        pass

    else:

        initial_search_input_info = [
            ('RA in deg', 'observation', 'ra_pointing', RANGE, None, None, False, 0, ''),
            ('Dec in deg', 'observation', 'dec_pointing', RANGE, None, None, False, 1, ''),
            ('Elevation in deg', 'observation', 'elevation_pointing', RANGE, None, None, False, 2, ''),
            ('Azimuth in deg', 'observation', 'azimuth_pointing', RANGE, None, None, False, 3, ''),
            ('Gridpoint number', 'observation', 'azimuth_pointing', RANGE, None, None, False, 4, ''),
        ]

        for search_input_info in initial_search_input_info:
            SearchInput.objects.create(
                search_input_group=info_group,
                display_name=search_input_info[0],
                table_name=search_input_info[1],
                field_name=search_input_info[2],
                field_type=search_input_info[3],
                initial_value=search_input_info[4],
                placeholder=search_input_info[5],
                required=search_input_info[6],
                display_order=search_input_info[7],
                input_info=search_input_info[8],
            )

    # inserting the fields for Time Constraints
    try:
        info_group = SearchInputGroup.objects.get(name='Time Constraints')

    except SearchInputGroup.DoesNotExist:
        pass

    else:

        initial_search_input_info = [
            ('Starttime in GPS seconds', 'observation', 'starttime', RANGE, None, None, False, 0, ''),
            # missing one here
            ('Obs duration, in seconds', 'observation', 'duration_sec', RANGE, None, None, False, 2, ''),
            ('Future', 'observation', 'starttime', RANGE, None, None, False, 3,
             'Check to find observations in the future, rather than the past.'),
        ]

        for search_input_info in initial_search_input_info:
            SearchInput.objects.create(
                search_input_group=info_group,
                display_name=search_input_info[0],
                table_name=search_input_info[1],
                field_name=search_input_info[2],
                field_type=search_input_info[3],
                initial_value=search_input_info[4],
                placeholder=search_input_info[5],
                required=search_input_info[6],
                display_order=search_input_info[7],
                input_info=search_input_info[8],
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
