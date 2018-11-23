"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.db import migrations

from mwasurveyweb.constants import *
from mwasurveyweb.models import SearchInput as SInput


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
            ('observation_name', 'Observation Name', 'observation', 'obsname', SInput.TEXT, TEXT, None, None, False, ''),
            ('creator', 'Creator', 'observation', 'creator', SInput.TEXT, TEXT, None, None, False, ''),
            ('calibration', 'Calibration', 'observation', 'calibration', SInput.BOOL, CHECKBOX, None, None, False, 'Check to find observations flagged as calibrators.'),
            ('calibrators', 'Calibrators', 'observation', 'calibrators', SInput.TEXT, TEXT, None, None, False, ''),
            ('cal_obs_id', 'Calibration Observation ID', 'observation', 'cal_obs_id', SInput.INT, NUMBER, None, None, False, ''),
            ('peelsrcs', 'Peel Sources', 'observation', 'peelsrcs', SInput.TEXT, TEXT, None, None, False, ''),
            ('ion_phs_peak', 'Ionosphere Phase Peak (Absolute)', 'observation', 'ion_phs_peak', SInput.INT, MAX_ABSOLUTE_NUMBER, '20', None, False, ''),
            ('ion_phs_std', 'Ionosphere Phase Standard', 'observation', 'ion_phs_std', SInput.INT, MAX_NUMBER, '90', None, False, ''),
            ('archived', 'Archived?', 'observation', 'archived', SInput.BOOL, CHECKBOX, None, None, False, ''),
            ('status', 'Status', 'observation', 'status', SInput.TEXT, SELECT, None, None, False, ''),
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
                input_type=search_input_info[5],
                initial_value=search_input_info[6],
                placeholder=search_input_info[7],
                required=search_input_info[8],
                input_info=search_input_info[9],
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
            ('ra', 'RA in deg', 'observation', 'ra_pointing', SInput.FLOAT, RADIUS, None, None, False, ''),
            ('dec', 'Dec in deg', 'observation', 'dec_pointing', SInput.FLOAT, RADIUS, None, None, False, ''),
            ('elevation', 'Elevation in deg', 'observation', 'elevation_pointing', SInput.FLOAT, RANGE, None, None, False, ''),
            ('azimuth', 'Azimuth in deg', 'observation', 'azimuth_pointing', SInput.FLOAT, RANGE, None, None, False, ''),
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
                input_type=search_input_info[5],
                initial_value=search_input_info[6],
                placeholder=search_input_info[7],
                required=search_input_info[8],
                input_info=search_input_info[9],
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
            ('start_time_gps', 'Starttime in GPS seconds', 'observation', 'starttime', SInput.TEXTTIME, RANGE, None, None, False, ''),
            ('start_time', 'Starttime in UTC', 'observation', 'starttime', SInput.TEXTTIME, DATE_RANGE, None, None, False, ''),
            ('obs_duration', 'Obs duration, in seconds', 'observation', 'duration_sec', SInput.INT, RANGE, None, None, False, ''),
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
                input_type=search_input_info[5],
                initial_value=search_input_info[6],
                placeholder=search_input_info[7],
                required=search_input_info[8],
                input_info=search_input_info[9],
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
            ('cenchan', 'Central Channel Number', 'observation', 'cenchan', SInput.INT, SELECT, '121', None, False, ''),
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
                input_type=search_input_info[5],
                initial_value=search_input_info[6],
                placeholder=search_input_info[7],
                required=search_input_info[8],
                input_info=search_input_info[9],
                display_order=display_order,
            )

            # update display order
            display_order += 1

    # inserting select input options for status
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

    # inserting select input options for cenchan
    search_input_options_info = [
        ('cenchan', '121', '154 MHz'),
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
