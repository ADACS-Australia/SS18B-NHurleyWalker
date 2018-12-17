"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.db import migrations


def insert(apps, schema_editor):
    SkyPlotsConfiguration = apps.get_model('mwasurveyweb', 'SkyPlotsConfiguration')
    Colour = apps.get_model('mwasurveyweb', 'Colour')

    colour_codes = [
        ('yellow', 'FFD700'),
        ('light-grey', '808080'),
        ('blue', '4169E1'),
    ]

    for colour_code in colour_codes:
        Colour.objects.create(
            name=colour_code[0],
            code=colour_code[1],
        )

    observation_statuses = [
        ('unprocessed', 'light-grey'),
        ('downloaded', 'yellow'),
        ('calibrated', 'yellow'),
        ('imaged', 'yellow'),
        ('archived', 'blue'),
    ]

    for observation_status in observation_statuses:
        SkyPlotsConfiguration.objects.create(
            observation_status=observation_status[0],
            colour=Colour.objects.get(name=observation_status[1]),
        )


def revert(apps, schema_editor):
    Colour = apps.get_model('mwasurveyweb', 'Colour')

    Colour.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('mwasurveyweb', '0007_auto_20181217_1841'),
    ]

    operations = [
        migrations.RunPython(code=insert, reverse_code=revert)
    ]
