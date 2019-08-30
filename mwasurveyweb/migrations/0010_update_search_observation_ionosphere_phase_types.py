"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.db import migrations

from mwasurveyweb import constants


def update(apps, schema_editor):
    SearchInput = apps.get_model('mwasurveyweb', 'SearchInput')
    SearchInputGroup = apps.get_model('mwasurveyweb', 'SearchInputGroup')

    info_group = SearchInputGroup.objects.get(name='observation_observation_info')

    search_input = SearchInput.objects.get(
        search_input_group=info_group,
        name='ion_phs_peak',
        table_name='observation',
        field_name='ion_phs_peak'
    )

    search_input.initial_value = ''
    search_input.input_type = constants.RANGE_INT
    search_input.save()

    search_input = SearchInput.objects.get(
        search_input_group=info_group,
        name='ion_phs_std',
        table_name='observation',
        field_name='ion_phs_std'
    )

    search_input.initial_value = ''
    search_input.input_type = constants.RANGE_INT
    search_input.save()


def revert(apps, schema_editor):
    SearchInput = apps.get_model('mwasurveyweb', 'SearchInput')
    SearchInputGroup = apps.get_model('mwasurveyweb', 'SearchInputGroup')

    info_group = SearchInputGroup.objects.get(name='observation_observation_info')

    search_input = SearchInput.objects.get(
        search_input_group=info_group,
        name='ion_phs_peak',
        table_name='observation',
        field_name='ion_phs_peak'
    )

    search_input.initial_value = '20'
    search_input.input_type = constants.MAX_ABSOLUTE_NUMBER
    search_input.save()

    search_input = SearchInput.objects.get(
        search_input_group=info_group,
        name='ion_phs_std',
        table_name='observation',
        field_name='ion_phs_std'
    )

    search_input.initial_value = '90'
    search_input.input_type = constants.MAX_NUMBER
    search_input.save()


class Migration(migrations.Migration):

    dependencies = [
        ('mwasurveyweb', '0009_auto_20190830_1605'),
    ]

    operations = [
        migrations.RunPython(code=update, reverse_code=revert)
    ]
