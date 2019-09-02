"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.db import migrations

from mwasurveyweb import constants


def update(apps, schema_editor):
    SearchInput = apps.get_model('mwasurveyweb', 'SearchInput')
    SearchInputGroup = apps.get_model('mwasurveyweb', 'SearchInputGroup')

    try:
        info_group = SearchInputGroup.objects.get(name='processing_time')

    except SearchInputGroup.DoesNotExist:
        pass

    else:

        search_input = SearchInput.objects.get(
            search_input_group=info_group,
            name='submission_time',
            table_name='processing',
            field_name='submission_time'
        )

        search_input.initial_value = ''
        search_input.input_type = constants.DATE_UNIX_RANGE
        search_input.save()

        search_input = SearchInput.objects.get(
            search_input_group=info_group,
            name='start_time',
            table_name='processing',
            field_name='start_time'
        )

        search_input.initial_value = ''
        search_input.input_type = constants.DATE_UNIX_RANGE
        search_input.save()

        search_input = SearchInput.objects.get(
            search_input_group=info_group,
            name='end_time',
            table_name='processing',
            field_name='end_time'
        )

        search_input.initial_value = ''
        search_input.input_type = constants.DATE_UNIX_RANGE
        search_input.save()


def revert(apps, schema_editor):
    SearchInput = apps.get_model('mwasurveyweb', 'SearchInput')
    SearchInputGroup = apps.get_model('mwasurveyweb', 'SearchInputGroup')

    try:
        info_group = SearchInputGroup.objects.get(name='processing_time')

    except SearchInputGroup.DoesNotExist:
        pass

    else:

        search_input = SearchInput.objects.get(
            search_input_group=info_group,
            name='submission_time',
            table_name='processing',
            field_name='submission_time'
        )

        search_input.initial_value = 'today'
        search_input.input_type = constants.DATE_UNIX
        search_input.save()

        search_input = SearchInput.objects.get(
            search_input_group=info_group,
            name='start_time',
            table_name='processing',
            field_name='start_time'
        )

        search_input.initial_value = 'today'
        search_input.input_type = constants.DATE_UNIX
        search_input.save()

        search_input = SearchInput.objects.get(
            search_input_group=info_group,
            name='end_time',
            table_name='processing',
            field_name='end_time'
        )

        search_input.initial_value = 'today'
        search_input.input_type = constants.DATE_UNIX
        search_input.save()


class Migration(migrations.Migration):

    dependencies = [
        ('mwasurveyweb', '0011_update_search_observation_cenchan_to_range'),
    ]

    operations = [
        migrations.RunPython(code=update, reverse_code=revert)
    ]
