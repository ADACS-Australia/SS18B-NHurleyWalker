"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.db import migrations


def insert(apps, schema_editor):
    SearchPage = apps.get_model('mwasurveyweb', 'SearchPage')
    SearchInputGroup = apps.get_model('mwasurveyweb', 'SearchInputGroup')
    SearchPageInputGroup = apps.get_model('mwasurveyweb', 'SearchPageInputGroup')

    initial_search_input_group_info = [
        ('observation', 'observation_info',),
        ('observation', 'pointing',),
        ('observation', 'time',),
        ('observation', 'observing_mode',),
    ]

    for search_page_input_group_info in initial_search_input_group_info:
        try:
            SearchPageInputGroup.objects.create(
                search_page=SearchPage.objects.get(name=search_page_input_group_info[0]),
                search_input_group=SearchInputGroup.objects.get(name=search_page_input_group_info[1]),
            )
        except (SearchPage.DoesNotExist, SearchInputGroup.DoesNotExist):
            continue


def revert(apps, schema_editor):
    SearchPageInputGroup = apps.get_model('mwasurveyweb', 'SearchPageInputGroup')

    SearchPageInputGroup.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('mwasurveyweb', '0004_insert_inputs'),
    ]

    operations = [
        migrations.RunPython(code=insert, reverse_code=revert)
    ]
