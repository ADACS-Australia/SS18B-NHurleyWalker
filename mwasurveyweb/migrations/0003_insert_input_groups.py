"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.db import migrations


def insert(apps, schema_editor):
    SearchInputGroup = apps.get_model('mwasurveyweb', 'SearchInputGroup')

    initial_search_input_info = [
        ('observation_observation_info', 'Observation Info Constraints', ''),
        ('observation_pointing', 'Pointing Constraints', ''),
        ('observation_time', 'Time Constraints', ''),
        ('observation_observing_mode', 'Observing Mode Constraints', ''),
    ]

    display_order = 0

    for search_input_info in initial_search_input_info:
        SearchInputGroup.objects.create(
            name=search_input_info[0],
            display_name=search_input_info[1],
            description=search_input_info[2],
            display_order=display_order,
        )

        # update display order
        display_order += 1

    initial_search_input_info = [
        ('processing_processing_info', 'Processing Info Constraints', ''),
        ('processing_time', 'Time Constraints', ''),
        ('processing_observation', 'Observation Constraints', ''),
    ]

    display_order = 100

    for search_input_info in initial_search_input_info:
        SearchInputGroup.objects.create(
            name=search_input_info[0],
            display_name=search_input_info[1],
            description=search_input_info[2],
            display_order=display_order,
        )

        # update display order
        display_order += 1


def revert(apps, schema_editor):
    SearchInputGroup = apps.get_model('mwasurveyweb', 'SearchInputGroup')

    SearchInputGroup.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('mwasurveyweb', '0002_insert_search_pages'),
    ]

    operations = [
        migrations.RunPython(code=insert, reverse_code=revert)
    ]
