"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

import sqlite3
import os

from django.conf import settings
from django.core.management import BaseCommand

from ...models import (
    SearchInputOption,
    SearchInputGroup,
    SearchInput,
)


class Command(BaseCommand):
    help = 'Loads all distinct users from the processing table and inserts as options for the select field on the ' \
           'search processing form'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        search_input_options_info = []

        try:

            conn = sqlite3.connect(settings.GLEAM_DATABASE_PATH)

            cursor = conn.cursor()

            query = 'SELECT DISTINCT user FROM processing'

            results = cursor.execute(query).fetchall()

            for result in results:
                search_input_options_info.append(('processing_processing_info', 'user', result[0], result[0]))

        except sqlite3.Error as e:
            print('{} in {}'.format(e, os.path.normpath(settings.GLEAM_DATABASE_PATH)))

        else:

            SearchInputOption.objects.filter(
                search_input__search_input_group__name='processing_processing_info',
                search_input__name='user',
            ).delete()

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
