"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.db import migrations

from mwasurveyweb import constants


def update(apps, schema_editor):
    SearchInput = apps.get_model('mwasurveyweb', 'SearchInput')
    SearchInputGroup = apps.get_model('mwasurveyweb', 'SearchInputGroup')
    SearchInputOption = apps.get_model('mwasurveyweb', 'SearchInputOption')

    info_group = SearchInputGroup.objects.get(name='observation_observing_mode')

    search_input = SearchInput.objects.get(
        search_input_group=info_group,
        name='cenchan',
        table_name='observation',
        field_name='cenchan'
    )

    search_input.initial_value = ''
    search_input.input_type = constants.RANGE
    search_input.save()

    SearchInputOption.objects.filter(
        search_input=SearchInput.objects.get(search_input_group=info_group,
                                             name='cenchan'),
    ).delete()


def revert(apps, schema_editor):
    SearchInput = apps.get_model('mwasurveyweb', 'SearchInput')
    SearchInputGroup = apps.get_model('mwasurveyweb', 'SearchInputGroup')
    SearchInputOption = apps.get_model('mwasurveyweb', 'SearchInputOption')

    info_group = SearchInputGroup.objects.get(name='observation_observing_mode')

    search_input = SearchInput.objects.get(
        search_input_group=info_group,
        name='cenchan',
        table_name='observation',
        field_name='cenchan'
    )

    search_input.initial_value = '121'
    search_input.input_type = constants.SELECT
    search_input.save()

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


class Migration(migrations.Migration):

    dependencies = [
        ('mwasurveyweb', '0010_update_search_observation_ionosphere_phase_types'),
    ]

    operations = [
        migrations.RunPython(code=update, reverse_code=revert)
    ]
