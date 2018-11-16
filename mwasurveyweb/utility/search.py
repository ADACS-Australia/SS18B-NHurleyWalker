"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.core.exceptions import ValidationError
from django.db.models import Q

from .utils import (
    check_forms_validity,
    get_operator_by_field_type,
)

from ..models import (
    SearchInput,
    SearchPageDisplayColumn,
)

from ..forms.search_parameter import SearchParameterForm
from ..forms.search import SearchForm


class SearchQuery(object):
    def _generate_query(self, form_type):

        # forming the subquery for the total count
        self.query_count = 'SELECT count(*) total ' \
                           'FROM {0} '.format(form_type)

        temp_query_condition = []
        for db_search_parameter in self.database_search_parameters:
            temp_query_part = '(' + db_search_parameter.get('table')
            temp_query_part += '.' + db_search_parameter.get('field')
            temp_query_part += ' ' + db_search_parameter.get('operator')
            temp_query_part += ' ?)'

            temp_query_condition.append(temp_query_part)
            self.query_values.append(db_search_parameter.get('value'))

        # subquery formation done
        if temp_query_condition:
            self.query_count = self.query_count + 'WHERE ' + ' AND '.join(temp_query_condition)

        # query select information
        table_columns = SearchPageDisplayColumn.objects.filter(Q(active=True), Q(search_page__name=form_type)) \
            .order_by('display_order')

        self.display_headers = []

        query_substring = ''

        for table_column in table_columns:
            self.display_headers.append(table_column.field_name)
            query_substring += '{table_name}.{field_name}, '.format(
                table_name=table_column.table_name,
                field_name=table_column.field_name,
            )

        self.query = 'SELECT {select_fields}' \
                     'subtable.total ' \
                     'FROM {table}, ({query_count}) subtable '.format(select_fields=query_substring,
                                                                      table=form_type,
                                                                      query_count=self.query_count,
                                                                      )

        if temp_query_condition:
            self.query = self.query + 'WHERE ' + ' AND '.join(temp_query_condition)

        # add up search parameters here
        self.query = self.query + self.search_parameter_order_by + self.search_parameter_limit

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

    def _process_search_parameters(self, cleaned_data):

        order_by = 'ASC'

        for key, value in cleaned_data.items():

            if key == 'results_per_page':
                self.limit = value

            if key == 'descending':
                order_by = 'DESC' if value else 'ASC'

        self.search_parameter_order_by = self.search_parameter_order_by.format(order_by=order_by)
        self.search_parameter_limit = self.search_parameter_limit.format(limit=self.limit, offset=self.offset)

    def _process_query(self):

        for search_form in self.search_forms:

            form = search_form.get('form')
            cleaned_data = form.cleaned_data

            # handling search parameter form
            if type(form) is SearchParameterForm:
                self._process_search_parameters(cleaned_data)

            # handling database search forms
            if type(form) is SearchForm:
                for key, value in cleaned_data.items():
                    if value:
                        self._enlist_database_search_parameter(key, value)

    def get_query(self):
        return self.query, self.query_values, self.limit, self.offset, self.display_headers

    def __init__(self, search_forms, form_type):
        self.search_forms = search_forms
        self.query = None
        self.query_count = None
        self.query_values = []
        self.limit = 100
        self.offset = 0
        self.database_search_parameters = []
        self.display_headers = []
        self.search_parameter_order_by = ' ORDER BY obs_id {order_by}'
        self.search_parameter_limit = ' LIMIT {limit} OFFSET {offset}'

        if check_forms_validity(search_forms):
            self._process_query()
            self._generate_query(form_type)
        else:
            raise ValidationError('Invalid input parameters')
