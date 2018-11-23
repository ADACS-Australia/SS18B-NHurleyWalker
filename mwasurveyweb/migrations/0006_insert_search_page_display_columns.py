"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.db import migrations


def insert(apps, schema_editor):
    SearchPage = apps.get_model('mwasurveyweb', 'SearchPage')
    SearchPageDisplayColumn = apps.get_model('mwasurveyweb', 'SearchPageDisplayColumn')

    initial_search_input_group_info = [
        ('observation', 'observation', 'starttime', 'GPS ID', ),
        ('observation', 'observation', 'obsname', 'Observation Name', ),
        ('observation', 'observation', 'ra_pointing', 'RA', ),
        ('observation', 'observation', 'dec_pointing', 'Dec', ),
        ('observation', 'observation', 'cenchan', 'Central Channel Number', ),
        ('observation', 'observation', 'ion_phs_peak', 'Ionosphere Phase Peak', ),
        ('observation', 'observation', 'status', 'Status', ),
    ]

    display_order = 0

    for search_page_display_column_info in initial_search_input_group_info:
        try:
            SearchPageDisplayColumn.objects.create(
                search_page=SearchPage.objects.get(name=search_page_display_column_info[0]),
                table_name=search_page_display_column_info[1],
                field_name=search_page_display_column_info[2],
                display_name=search_page_display_column_info[3],
                display_order=display_order,
            )

            display_order += 1
        except SearchPage.DoesNotExist:
            continue


def revert(apps, schema_editor):
    SearchPageDisplayColumn = apps.get_model('mwasurveyweb', 'SearchPageDisplayColumn')

    SearchPageDisplayColumn.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('mwasurveyweb', '0005_insert_search_page_input_groups'),
    ]

    operations = [
        migrations.RunPython(code=insert, reverse_code=revert)
    ]
