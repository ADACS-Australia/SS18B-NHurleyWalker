"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.core.exceptions import ValidationError

from .utils import (
    check_forms_validity,
    get_operator_by_field_type,
)

from ..models import (
    SearchInput,
)

from ..forms.search_parameter import SearchParameterForm
from ..forms.search import SearchForm


class SearchQuery(object):

    def _generate_query(self):
        self.query = 'SELECT * FROM observation WHERE '

        temp_query_condition = []
        for db_search_parameter in self.database_search_parameters:

            temp_query_part = '(' + db_search_parameter.get('table')
            temp_query_part += '.' + db_search_parameter.get('field')
            temp_query_part += ' ' + db_search_parameter.get('operator')
            temp_query_part += ' ?)'

            temp_query_condition.append(temp_query_part)
            self.query_values.append(db_search_parameter.get('value'))

        self.query = self.query + ' AND '.join(temp_query_condition)

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

        operator = get_operator_by_field_type(search_input.field_type, index)

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
        return self.query, self.query_values

    def __init__(self, search_forms):
        self.search_forms = search_forms
        self.query = None
        self.query_values = []
        self.database_search_parameters = []

        if check_forms_validity(search_forms):
            self._process_query()
            self._generate_query()
        else:
            raise ValidationError('Invalid input parameters')
