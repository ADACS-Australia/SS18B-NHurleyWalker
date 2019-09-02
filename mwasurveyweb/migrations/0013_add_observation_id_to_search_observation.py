"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.db import migrations

from mwasurveyweb import constants
from mwasurveyweb.models import SearchInput as SInput


def update(apps, schema_editor):
    SearchInput = apps.get_model('mwasurveyweb', 'SearchInput')
    SearchInputGroup = apps.get_model('mwasurveyweb', 'SearchInputGroup')

    try:
        info_group = SearchInputGroup.objects.get(name='observation_observation_info')

    except SearchInputGroup.DoesNotExist:
        pass

    else:

        # increase current order to create space for the observation_id input
        search_inputs = SearchInput.objects.filter(search_input_group=info_group).order_by('-display_order')

        for search_input in search_inputs:
            display_order = search_input.display_order + 1
            search_input.display_order = display_order
            search_input.save()

        initial_search_input_info = [
            ('observation_id', 'Observation ID', 'observation', 'obs_id', SInput.INT, constants.NUMBER, None, None,
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


def revert(apps, schema_editor):
    SearchInput = apps.get_model('mwasurveyweb', 'SearchInput')
    SearchInputGroup = apps.get_model('mwasurveyweb', 'SearchInputGroup')

    # inserting the fields for Observation Info Constraints
    try:
        info_group = SearchInputGroup.objects.get(name='observation_observation_info')

    except SearchInputGroup.DoesNotExist:
        pass

    else:

        SearchInput.objects.filter(
            search_input_group=info_group,
            name='observation_id',
            display_name='Observation ID',
            table_name='observation',
            field_name='obs_id',
        ).delete()

        # decrease current order to create space for the observation_id input
        search_inputs = SearchInput.objects.filter(search_input_group=info_group).order_by('display_order')

        for search_input in search_inputs:
            display_order = search_input.display_order - 1
            search_input.display_order = display_order
            search_input.save()


class Migration(migrations.Migration):

    dependencies = [
        ('mwasurveyweb', '0012_update_search_processing_dates_to_date_range'),
    ]

    operations = [
        migrations.RunPython(code=update, reverse_code=revert)
    ]
