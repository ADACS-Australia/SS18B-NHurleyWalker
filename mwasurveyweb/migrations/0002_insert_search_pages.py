"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.db import migrations


def insert(apps, schema_editor):
    SearchPage = apps.get_model('mwasurveyweb', 'SearchPage')

    initial_search_page_info = [
        ('observation', 'Observation'),
        ('processing', 'Processing'),
    ]

    display_order = 0

    for search_page in initial_search_page_info:
        SearchPage.objects.create(
            name=search_page[0],
            display_name=search_page[1],
            display_order=display_order,
        )

        # update display order
        display_order += 1


def revert(apps, schema_editor):
    SearchPage = apps.get_model('mwasurveyweb', 'SearchPage')

    SearchPage.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('mwasurveyweb', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(code=insert, reverse_code=revert)
    ]
