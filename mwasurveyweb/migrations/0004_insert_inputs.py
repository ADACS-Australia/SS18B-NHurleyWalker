"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

import sqlite3
import os

from django.conf import settings
from django.db import migrations

from mwasurveyweb.constants import *
from mwasurveyweb.models import SearchInput as SInput


def insert(apps, schema_editor):
    SearchInputGroup = apps.get_model('mwasurveyweb', 'SearchInputGroup')

    SearchInput = apps.get_model('mwasurveyweb', 'SearchInput')

    SearchInputOption = apps.get_model('mwasurveyweb', 'SearchInputOption')

    # inserting the fields for Observation Info Constraints
    try:
        info_group = SearchInputGroup.objects.get(name='observation_observation_info')

    except SearchInputGroup.DoesNotExist:
        pass

    else:

        initial_search_input_info = [
            ('observation_name', 'Observation Name', 'observation', 'obsname', SInput.TEXT, TEXT, None, None, False,
             ''),
            ('creator', 'Creator', 'observation', 'creator', SInput.TEXT, TEXT, None, None, False, ''),
            ('calibration', 'Calibration', 'observation', 'calibration', SInput.BOOL, CHECKBOX, None, None, False,
             'Check to find observations flagged as calibrators.'),
            ('calibrators', 'Calibrators', 'observation', 'calibrators', SInput.TEXT, TEXT, None, None, False, ''),
            ('cal_obs_id', 'Calibration Observation ID', 'observation', 'cal_obs_id', SInput.INT, NUMBER, None, None,
             False, ''),
            ('peelsrcs', 'Peel Sources', 'observation', 'peelsrcs', SInput.TEXT, TEXT, None, None, False, ''),
            ('ion_phs_peak', 'Ionosphere Phase Peak (Absolute)', 'observation', 'ion_phs_peak', SInput.INT,
             MAX_ABSOLUTE_NUMBER, '20', None, False, ''),
            ('ion_phs_std', 'Ionosphere Phase Standard', 'observation', 'ion_phs_std', SInput.INT, MAX_NUMBER, '90',
             None, False, ''),
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
        info_group = SearchInputGroup.objects.get(name='observation_pointing')

    except SearchInputGroup.DoesNotExist:
        pass

    else:

        initial_search_input_info = [
            ('ra', 'RA in deg', 'observation', 'ra_pointing', SInput.FLOAT, RADIUS, None, None, False, ''),
            ('dec', 'Dec in deg', 'observation', 'dec_pointing', SInput.FLOAT, RADIUS, None, None, False, ''),
            ('elevation', 'Elevation in deg', 'observation', 'elevation_pointing', SInput.FLOAT, RANGE, None, None,
             False, ''),
            ('azimuth', 'Azimuth in deg', 'observation', 'azimuth_pointing', SInput.FLOAT, RANGE, None, None, False,
             ''),
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
        info_group = SearchInputGroup.objects.get(name='observation_time')

    except SearchInputGroup.DoesNotExist:
        pass

    else:

        initial_search_input_info = [
            ('start_time', 'Starttime in UTC', 'observation', 'starttime', SInput.TEXTTIME, DATE_RANGE,
             '01/01/2018,31/07/2018', None, False, ''),
            ('obs_duration', 'Obs duration, in seconds', 'observation', 'duration_sec', SInput.INT, RANGE, None, None,
             False, ''),
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
        info_group = SearchInputGroup.objects.get(name='observation_observing_mode')

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
        ('observation_observation_info', 'status', 'unprocessed', 'Unprocessed'),
        ('observation_observation_info', 'status', 'downloaded', 'Downloaded'),
        ('observation_observation_info', 'status', 'calibrated', 'Calibrated'),
        ('observation_observation_info', 'status', 'imaged', 'Imaged'),
        ('observation_observation_info', 'status', 'archived', 'Archived'),
    ]

    display_order = 0

    for search_input_option in search_input_options_info:
        try:
            search_input_group = SearchInputGroup.objects.get(name=search_input_option[0])

            SearchInputOption.objects.create(
                search_input=SearchInput.objects.get(search_input_group=search_input_group,
                                                     name=search_input_option[1]),
                name=search_input_option[2],
                display_name=search_input_option[3],
                display_order=display_order,
            )

            # update display order
            display_order += 1

        except (SearchInputGroup.DoesNotExist, SearchInput.DoesNotExist):
            continue

    # inserting select input options for cenchan
    search_input_options_info = [
        ('observation_observing_mode', 'cenchan', '69', '88 MHz'),
        ('observation_observing_mode', 'cenchan', '93', '119 MHz'),
        ('observation_observing_mode', 'cenchan', '121', '154 MHz'),
        ('observation_observing_mode', 'cenchan', '145', '185 MHz'),
        ('observation_observing_mode', 'cenchan', '169', '216 MHz'),
    ]

    display_order = 0

    for search_input_option in search_input_options_info:
        try:
            search_input_group = SearchInputGroup.objects.get(name=search_input_option[0])

            SearchInputOption.objects.create(
                search_input=SearchInput.objects.get(search_input_group=search_input_group,
                                                     name=search_input_option[1]),
                name=search_input_option[2],
                display_name=search_input_option[3],
                display_order=display_order,
            )

            # update display order
            display_order += 1

        except (SearchInputGroup.DoesNotExist, SearchInput.DoesNotExist):
            continue

    # ################################
    # # START PROCESSING FORM INPUTS #
    # ################################

    # inserting the fields for Processing Info Constraints
    try:
        info_group = SearchInputGroup.objects.get(name='processing_processing_info')

    except SearchInputGroup.DoesNotExist:
        pass

    else:

        initial_search_input_info = [
            ('job_id', 'Job ID', 'processing', 'job_id', SInput.INT, NUMBER, None, None, False, ''),
            ('task', 'Task', 'processing', 'task', SInput.TEXT, SELECT, None, None, False, ''),
            ('user', 'User', 'processing', 'user', SInput.TEXT, SELECT, None, None, False, ''),
            ('status', 'Status', 'processing', 'status', SInput.TEXT, SELECT, None, None, False, ''),
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

    # inserting the fields for Processing Time Constraints
    try:
        info_group = SearchInputGroup.objects.get(name='processing_time')

    except SearchInputGroup.DoesNotExist:
        pass

    else:

        initial_search_input_info = [
            ('submission_time', 'Submission Time', 'processing', 'submission_time', SInput.INT, DATE, 'today', None,
             False, ''),
            ('start_time', 'Start Time', 'processing', 'start_time', SInput.INT, DATE, 'today', None, False, ''),
            ('end_time', 'End Time', 'processing', 'end_time', SInput.INT, DATE, 'today', None, False, ''),
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

    # inserting the fields for Processing Observation Constraints
    try:
        info_group = SearchInputGroup.objects.get(name='processing_observation')

    except SearchInputGroup.DoesNotExist:
        pass

    else:

        initial_search_input_info = [
            ('obs_id', 'Observation ID', 'processing', 'obs_id', SInput.INT, NUMBER, None, None, False, ''),
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

    # inserting select input options for task
    search_input_options_info = [
        ('processing_processing_info', 'task', 'download', 'Download'),
        ('processing_processing_info', 'task', 'calibrate', 'Calibrate'),
        ('processing_processing_info', 'task', 'apply_cal', 'Apply Calibration'),
        ('processing_processing_info', 'task', 'check_srcs', 'Check Sources'),
        ('processing_processing_info', 'task', 'cotter', 'Cotter'),
        ('processing_processing_info', 'task', 'image', 'Image'),
        ('processing_processing_info', 'task', 'archive', 'Archive'),
    ]

    display_order = 0

    for search_input_option in search_input_options_info:
        try:
            search_input_group = SearchInputGroup.objects.get(name=search_input_option[0])

            SearchInputOption.objects.create(
                search_input=SearchInput.objects.get(search_input_group=search_input_group,
                                                     name=search_input_option[1]),
                name=search_input_option[2],
                display_name=search_input_option[3],
                display_order=display_order,
            )

            # update display order
            display_order += 1

        except (SearchInputGroup.DoesNotExist, SearchInput.DoesNotExist):
            continue

    # inserting select input options for status
    search_input_options_info = [
        ('processing_processing_info', 'status', 'queued', 'Queued'),
        ('processing_processing_info', 'status', 'started', 'Started'),
        ('processing_processing_info', 'status', 'finished', 'Finished'),
        ('processing_processing_info', 'status', 'failed', 'Failed'),
    ]

    display_order = 0

    for search_input_option in search_input_options_info:
        try:
            search_input_group = SearchInputGroup.objects.get(name=search_input_option[0])

            SearchInputOption.objects.create(
                search_input=SearchInput.objects.get(search_input_group=search_input_group,
                                                     name=search_input_option[1]),
                name=search_input_option[2],
                display_name=search_input_option[3],
                display_order=display_order,
            )

            # update display order
            display_order += 1

        except (SearchInputGroup.DoesNotExist, SearchInput.DoesNotExist):
            continue

    # inserting select input options for the users
    search_input_options_info = []

    try:

        conn = sqlite3.connect(settings.GLEAM_DATABASE_PATH)

        cursor = conn.cursor()

        query = 'SELECT DISTINCT user FROM processing'

        results = cursor.execute(query).fetchall()

        for result in results:
            search_input_options_info.append(('processing_processing_info', 'user', result[0], result[0]))

    except sqlite3.Error as e:
        print('\n{} in {}'.format(e, os.path.normpath(settings.GLEAM_DATABASE_PATH)))

    else:

        SearchInputOption.objects.filter(
            search_input__search_input_group__name='processing_processing_info',
            search_input__name='user',
        ).delete()

        display_order = 0

        for search_input_option in search_input_options_info:
            try:
                search_input_group = SearchInputGroup.objects.get(name=search_input_option[0])

                SearchInputOption.objects.create(
                    search_input=SearchInput.objects.get(search_input_group=search_input_group,
                                                         name=search_input_option[1]),
                    name=search_input_option[2],
                    display_name=search_input_option[3],
                    display_order=display_order,
                )

                # update display order
                display_order += 1

            except (SearchInputGroup.DoesNotExist, SearchInput.DoesNotExist):
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
