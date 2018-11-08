"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.core.exceptions import ValidationError

from ..constants import *
from .utils import check_forms_validity
from ..models import (
    SearchInput,
)

from ..forms.search_parameter import SearchParameterForm
from ..forms.search import SearchForm


class SearchQuery(object):

    query = None
    database_search_parameters = []

    def _generate_query(self):
        self.query = 'SELECT * FROM observation WHERE'

    def _get_operator_by_field_type(self, field_type, index=None):
        if field_type == TEXT:
            return 'LIKE'

        if field_type == RANGE:
            if index == 0:
                return '>='
            if index == 1:
                return '<='

    def _enlist_database_search_parameter(self, key, value):
        input_properties = key.split('__')

        try:
            search_input = SearchInput.objects.get(
                search_input_group__name=input_properties[0],
                name=input_properties[1],
                active=True,
            )
        except SearchInput.DoesNotExist:
            return

        table = search_input.table_name
        field = search_input.field_name

        try:
            index = input_properties[2]
        except IndexError:
            index = None

        operator = self._get_operator_by_field_type(search_input.field_type, index)

        self.database_search_parameters.append(
            dict(
                table=table,
                field=field,
                operator=operator,
                value=value,
            )
        )

    def _process_query(self):

        for search_form in self.search_forms:

            form = search_form.get('form')
            cleaned_data = form.cleaned_data

            # handling search parameter form
            if type(form) is SearchParameterForm:
                pass

            # handling database search forms
            if type(form) is SearchForm:
                for key, value in cleaned_data.items():
                    if value:
                        self._enlist_database_search_parameter(key, value)

    def get_query(self):
        return self.query

    def __init__(self, search_forms):
        self.search_forms = search_forms

        if check_forms_validity(search_forms):
            self._process_query()
