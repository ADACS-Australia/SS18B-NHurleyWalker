"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.db import migrations

from mwasurveyweb.constants import *


def insert(apps, schema_editor):
    SearchInputGroup = apps.get_model('mwasurveyweb', 'SearchInputGroup')

    SearchInput = apps.get_model('mwasurveyweb', 'SearchInput')

    SearchInputOption = apps.get_model('mwasurveyweb', 'SearchInputOption')

    # inserting the fields for Observation Info Constraints
    try:
        info_group = SearchInputGroup.objects.get(name='observation_info')

    except SearchInputGroup.DoesNotExist:
        pass

    else:

        initial_search_input_info = [
            ('observation_name', 'Observation Name', 'observation', 'obsname', TEXT, None, None, False, ''),
            ('creator', 'Creator', 'observation', 'creator', TEXT, None, None, False, ''),
            ('calibration', 'Calibration', 'observation', 'calibration', CHECKBOX, None, None, False, 'Check to find observations flagged as calibrators.'),
            ('calibrators', 'Calibrators', 'observation', 'calibrators', TEXT, None, None, False, ''),
            ('cal_obs_id', 'CAL OBS ID', 'observation', 'cal_obs_id', NUMBER, None, None, False, ''),
            ('peelsrcs', 'peelsrcs', 'observation', 'peelsrcs', TEXT, None, None, False, ''),
            ('ion_phs_peak', 'ion phs peak', 'observation', 'ion_phs_peak', MAX_NUMBER, '20', None, False, ''),
            ('ion_phs_std', 'ion phs std', 'observation', 'ion_phs_std', MAX_NUMBER, '90', None, False, ''),
            ('archived', 'Archived?', 'observation', 'archived', CHECKBOX, None, None, False, ''),
            ('status', 'Status', 'observation', 'status', SELECT, None, None, False, ''),
        ]

        display_order = 0

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
                input_info=search_input_info[8],
                display_order=display_order,
            )

            # update display order
            display_order += 1

    # inserting the fields for Pointing Constraints
    try:
        info_group = SearchInputGroup.objects.get(name='pointing')

    except SearchInputGroup.DoesNotExist:
        pass

    else:

        initial_search_input_info = [
            ('ra', 'RA in deg', 'observation', 'ra_pointing', RADIUS, None, None, False, ''),
            ('dec', 'Dec in deg', 'observation', 'dec_pointing', RADIUS, None, None, False, ''),
            ('elevation', 'Elevation in deg', 'observation', 'elevation_pointing', RANGE, None, None, False, ''),
            ('azimuth', 'Azimuth in deg', 'observation', 'azimuth_pointing', RANGE, None, None, False, ''),
        ]

        display_order = 0

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
                input_info=search_input_info[8],
                display_order=display_order,
            )

            # update display order
            display_order += 1

    # inserting the fields for Time Constraints
    try:
        info_group = SearchInputGroup.objects.get(name='time')

    except SearchInputGroup.DoesNotExist:
        pass

    else:

        initial_search_input_info = [
            ('start_time_gps', 'Starttime in GPS seconds', 'observation', 'starttime', RANGE, None, None, False, ''),
            ('start_time', 'Starttime in UTC', 'observation', 'starttime', DATE_RANGE, None, None, False, ''),
            ('obs_duration', 'Obs duration, in seconds', 'observation', 'duration_sec', RANGE, None, None, False, ''),
            ('future', 'Future', 'observation', 'starttime', CHECKBOX, None, None, False, 'Check to find observations in the future, rather than the past.'),
        ]

        display_order = 0

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
                input_info=search_input_info[8],
                display_order=display_order,
            )

            # update display order
            display_order += 1

    # inserting the fields for Observing Mode Constraints
    try:
        info_group = SearchInputGroup.objects.get(name='observing_mode')

    except SearchInputGroup.DoesNotExist:
        pass

    else:

        initial_search_input_info = [
            (
            'cenchan', 'Central Channel Number', 'observation', 'cenchan', SELECT, '121', None, False, ''),
        ]

        display_order = 0

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
                input_info=search_input_info[8],
                display_order=display_order,
            )

            # update display order
            display_order += 1

    # inserting select input options
    search_input_options_info = [
        ('status', 'unprocessed', 'Unprocessed'),
        ('status', 'downloaded', 'Downloaded'),
        ('status', 'calibrated', 'Calibrated'),
        ('status', 'imaged', 'Imaged'),
        ('status', 'archived', 'Archived'),
    ]

    display_order = 0

    for search_input_option in search_input_options_info:
        try:
            SearchInputOption.objects.create(
                search_input=SearchInput.objects.get(name=search_input_option[0]),
                name=search_input_option[1],
                display_name=search_input_option[2],
                display_order=display_order,
            )

            # update display order
            display_order += 1

        except SearchInput.DoesNotExist:
            continue


def revert(apps, schema_editor):
    SearchInput = apps.get_model('mwasurveyweb', 'SearchInput')

    SearchInput.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('mwasurveyweb', '0003_insert_input_groups'),
    ]

    operations = [
        migrations.RunPython(code=insert, reverse_code=revert)
    ]
