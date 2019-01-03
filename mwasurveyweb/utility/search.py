"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db.models import Q

from .utils import (
    check_forms_validity,
    get_operator_by_input_type,
    get_gps_time_from_date,
    get_unix_time_from_date,
)

from ..models import (
    SearchInput,
    SearchPageDisplayColumn,
)

from ..forms.search_parameter import SearchParameterForm
from ..forms.search import SearchForm

from .. import constants


class SearchQuery(object):
    def _generate_query(self, form_type):

        # forming the subquery for the total count
        self.query_count = 'SELECT count(*) total ' \
                           'FROM {0} '.format(form_type)

        temp_query_condition = []
        for db_search_parameter in self.database_search_parameters:
            try:
                if db_search_parameter.get('field_operator', None):
                    temp_query_part = '({field_operator}({table}.{field}) {operator} ?)'.format(
                        field_operator=db_search_parameter.get('field_operator'),
                        table=db_search_parameter.get('table'),
                        field=db_search_parameter.get('field'),
                        operator=db_search_parameter.get('operator'),
                    )
                else:
                    temp_query_part = '({table}.{field} {operator} ?)'.format(
                        table=db_search_parameter.get('table'),
                        field=db_search_parameter.get('field'),
                        operator=db_search_parameter.get('operator'),
                    )

                temp_query_condition.append(temp_query_part)
                self.query_values.append(db_search_parameter.get('value'))
            except:
                pass

        # subquery formation done
        if temp_query_condition:
            self.query_count = self.query_count + 'WHERE ' + ' AND '.join(temp_query_condition)

        # query select information
        table_columns = SearchPageDisplayColumn.objects.filter(Q(active=True), Q(search_page__name=form_type)) \
            .order_by('display_order')

        self.display_headers = []

        query_substring = ''

        for table_column in table_columns:
            self.display_headers.append(
                dict(
                    display=table_column.display_name,
                    field_name=table_column.field_name,
                    sort_order='',
                )
            )

            query_substring += '{table_name}.{field_name}, '.format(
                table_name=table_column.table_name,
                field_name=table_column.field_name,
            )

        self.query = \
            'SELECT {select_fields}' \
            'subtable.total ' \
            'FROM {table}, ({query_count}) subtable '.format(
                select_fields=query_substring,
                table=form_type,
                query_count=self.query_count,
            )

        if temp_query_condition:
            self.query = self.query + 'WHERE ' + ' AND '.join(temp_query_condition)

        # add up search parameters here
        self.query = self.query + self.search_parameter_order_by + self.search_parameter_limit

    def _update_database_search_parameter(self, value, search_input, search_form, input_properties):
        try:
            index = input_properties[2]
        except IndexError:
            index = None

        value_adjusted = value

        try:
            if search_input.input_type in [constants.DATE_GPS, constants.DATE_GPS_RANGE, ]:
                value_adjusted = get_gps_time_from_date(value_adjusted)

            if search_input.input_type in [constants.DATE_UNIX, constants.DATE_UNIX_RANGE]:
                value_adjusted = get_unix_time_from_date(value_adjusted)

            if search_input.field_type == SearchInput.INT:
                value_adjusted = int(value_adjusted)
            elif search_input.field_type == SearchInput.FLOAT:
                value_adjusted = float(value_adjusted)
            elif search_input.field_type == SearchInput.BOOL:
                value_adjusted = 1 if value_adjusted else 0
        except (TypeError, ValueError):
            pass

        radius_value = 0  # for Non RADIUS inputs it does not matter

        # finding appropriate value for RADIUS input types
        if search_input.input_type == constants.RADIUS:
            field_name = '__'.join(input_properties[:-1] + ['1' if input_properties[2] == '0' else '0'])

            radius_value = search_form['form'].cleaned_data.get(field_name) \
                if search_form['form'].cleaned_data.get(field_name) else 0

            if search_input.field_type == SearchInput.INT:
                radius_value_adjusted = int(radius_value)
            elif search_input.field_type == SearchInput.FLOAT:
                radius_value_adjusted = float(radius_value)
            else:
                radius_value_adjusted = radius_value

            value_adjusted += radius_value_adjusted * (-1 if input_properties[2] == '0' else 1)

        operator, field_operator = get_operator_by_input_type(search_input.input_type, index, second_value=radius_value)

        self.database_search_parameters.append(
            dict(
                table=search_input.table_name,
                field=search_input.field_name,
                field_operator=field_operator,
                operator=operator,
                value=value_adjusted,
            )
        )

    def _enlist_database_search_parameter(self, key, value, search_form):

        input_properties = key.split('__')

        try:
            search_input = SearchInput.objects.get(
                search_input_group__name=input_properties[0],
                name=input_properties[1],
                active=True,
            )
        except SearchInput.DoesNotExist:
            return

        self._update_database_search_parameter(
            value=value,
            search_input=search_input,
            search_form=search_form,
            input_properties=input_properties,
        )

        # Because a date is converted to a specific second (ex: 01/01/2008 is actually 01/01/2008 00:00:00:000),
        # anything that has been on that day need be evaluated as a range, meaning for the above example:
        # we should search for anything between 01/01/2008 00:00:00:000 to 02/01/2008 00:00:00:000. To achieve that,
        # another query constraint is needed to be added with the index 1.
        if search_input.input_type in [constants.DATE_GPS, constants.DATE_UNIX, ]:
            self._update_database_search_parameter(
                value=value + timedelta(days=1),
                search_input=search_input,
                search_form=search_form,
                input_properties=input_properties[:-1] + ['1'],
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
                        self._enlist_database_search_parameter(key, value, search_form)

    def get_query(self):
        return self.query, self.query_values, self.search_parameter_order_by, self.limit, self.offset, \
               self.display_headers

    def __init__(self, search_forms, form_type):
        self.search_forms = search_forms
        self.query = None
        self.query_count = None
        self.query_values = []
        self.limit = 100
        self.offset = 0
        self.database_search_parameters = []
        self.display_headers = []

        if form_type == 'observation':
            self.search_parameter_order_by = ' ORDER BY starttime {order_by}'
        else:
            self.search_parameter_order_by = ' ORDER BY job_id {order_by}'

        self.search_parameter_limit = ' LIMIT {limit} OFFSET {offset}'

        if check_forms_validity(search_forms):
            self._process_query()
            self._generate_query(form_type)
        else:
            raise ValidationError('Invalid input parameters')
