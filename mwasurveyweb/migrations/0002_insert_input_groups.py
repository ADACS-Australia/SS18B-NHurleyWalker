"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.db import migrations


def insert(apps, schema_editor):
    SearchInputGroup = apps.get_model('mwasurveyweb', 'SearchInputGroup')

    initial_search_input_info = [
        ('Observation Info Constraints', '', 0),
        ('Pointing Constraints', '', 1),
        ('Time Constraints', '', 2),
        ('Observing Mode Constraints', '', 3),
    ]

    for search_input_info in initial_search_input_info:
        SearchInputGroup.objects.create(
            name=search_input_info[0],
            description=search_input_info[1],
            display_order=search_input_info[2],
        )


def revert(apps, schema_editor):
    SearchInputGroup = apps.get_model('mwasurveyweb', 'SearchInputGroup')

    SearchInputGroup.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('mwasurveyweb', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(code=insert, reverse_code=revert)
    ]
