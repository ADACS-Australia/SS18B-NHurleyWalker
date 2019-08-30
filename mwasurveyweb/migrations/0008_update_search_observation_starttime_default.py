"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.db import migrations


def update(apps, schema_editor):
    SearchInput = apps.get_model('mwasurveyweb', 'SearchInput')
    SearchInputGroup = apps.get_model('mwasurveyweb', 'SearchInputGroup')

    start_time = SearchInput.objects.get(
        search_input_group=SearchInputGroup.objects.get(name='observation_time'),
        name='start_time',
        table_name='observation',
        field_name='starttime'
    )

    start_time.initial_value = '01/08/2013,today'
    start_time.save()


def revert(apps, schema_editor):
    SearchInput = apps.get_model('mwasurveyweb', 'SearchInput')
    SearchInputGroup = apps.get_model('mwasurveyweb', 'SearchInputGroup')

    start_time = SearchInput.objects.get(
        search_input_group=SearchInputGroup.objects.get(name='observation_time'),
        name='start_time',
        table_name='observation',
        field_name='starttime'
    )

    start_time.initial_value = '01/01/2018,31/07/2018'
    start_time.save()


class Migration(migrations.Migration):

    dependencies = [
        ('mwasurveyweb', '0007_insert_skyplot_configurations'),
    ]

    operations = [
        migrations.RunPython(code=update, reverse_code=revert)
    ]
