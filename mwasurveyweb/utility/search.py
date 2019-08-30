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
    """
    Class to generate query from the user inputs. This uses search forms to find out what has been queried and then
    formulates the search query accordingly.
    """

    def _generate_query(self, form_type):
        """
        Once processing query is finished, query is generated from the search parameters.
        :param form_type: string defines the type of the form, ex: 'observation' or 'processing'
        """

        # forming the subquery for the total count
        self.query_count = 'SELECT count(*) total ' \
                           'FROM {0} '.format(form_type)

        temp_query_condition = []

        # from the database_search_parameters forming the conditions
        # a condition can be in the following forms:
        # 1. count(a.b) > ?
        # 2. a.b > ?
        # later during execution the ? will be replaced by the values by the cursor
        for db_search_parameter in self.database_search_parameters:
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

            # appending the query conditions and their corresponding values
            temp_query_condition.append(temp_query_part)
            self.query_values.append(db_search_parameter.get('value'))

        # subquery formation
        if temp_query_condition:
            self.query_count = self.query_count + 'WHERE ' + ' AND '.join(temp_query_condition)

        # query select information, this is different than count query. This retrieves the required information
        # based on the configuration set in the database.
        # finding the search page table and columns from the database
        table_columns = SearchPageDisplayColumn.objects.filter(Q(active=True), Q(search_page__name=form_type)) \
            .order_by('display_order')

        self.display_headers = []

        query_substring = ''

        # forming the query substring and also display headers
        for table_column in table_columns:
            self.display_headers.append(
                dict(
                    display=table_column.display_name,  # what is displayed in the UI.
                    field_name=table_column.field_name,  # actual field that is referenced to.
                    sort_order='',  # to show which order they are displayed currently. Initially it is not ordered.
                )
            )

            query_substring += '{table_name}.{field_name}, '.format(
                table_name=table_column.table_name,
                field_name=table_column.field_name,
            )

        # forming the final query including total count up to the condition part
        self.query = \
            'SELECT {select_fields}' \
            'subtable.total ' \
            'FROM {table}, ({query_count}) subtable '.format(
                select_fields=query_substring,
                table=form_type,
                query_count=self.query_count,
            )

        # adding the condition part if required. Otherwise, nothing will be added.
        if temp_query_condition:
            self.query = self.query + 'WHERE ' + ' AND '.join(temp_query_condition)

        # add up search parameters here
        self.query = self.query + self.search_parameter_order_by + self.search_parameter_limit

    def _update_database_search_parameter(self, value, search_input, search_form, input_properties):
        """
        Creates a database search parameter parameters for a particular search input and value.
        Finds the operator and field operators based and constructs a dictionary to facilitate query clause formation.
        Ex: for a query clause count(a.b) > c
        'a.b' is the table.field
        'c' is the value adjusted
        'count' is the field_operator
        '>' is the operator
        These are later forms a dictionary and appended to the database_search_parameters list.
        :param value: input value by the user
        :param search_input: search input instance
        :param search_form: search form that this input belongs to
        :param input_properties: list of input properties containing, group name, name and index
        """

        # setting up the index to `None` if it is not there.
        try:
            index = input_properties[2]
        except IndexError:
            index = None

        # adjusted value is set as value, if no adjustment needed, it will be unchanged
        value_adjusted = value

        # adjust the value based on the input type and field type
        try:

            # converting the value to gps time if input type is gps date or gps date range
            if search_input.input_type in [constants.DATE_GPS, constants.DATE_GPS_RANGE, ]:
                value_adjusted = get_gps_time_from_date(value_adjusted)

            # converting the value to unix timestamp if input type is unix date or unix date range
            if search_input.input_type in [constants.DATE_UNIX, constants.DATE_UNIX_RANGE]:
                value_adjusted = get_unix_time_from_date(value_adjusted)

            # converting the value based on the field type
            if search_input.field_type == SearchInput.INT:
                value_adjusted = int(value_adjusted)
            elif search_input.field_type == SearchInput.FLOAT:
                value_adjusted = float(value_adjusted)
            elif search_input.field_type == SearchInput.BOOL:
                value_adjusted = 1 if value_adjusted else 0
        except (TypeError, ValueError):
            pass

        radius_value = 0  # for Non RADIUS inputs it does not matter

        # finding appropriate value for RADIUS input types, because radius input is defined as
        # x, r where x is the centre and r is the radius which will be converted as a range input as follows:
        # a, b where a = x - r and b = x + r
        # A conversion like this requires two input values by the user, however, this function only gets one, that is:
        # x or r, so, for finding a or b from x or r only is not possible. Therefore, we need to find out the other
        # value to complete the calculation.
        if search_input.input_type == constants.RADIUS:

            # constructing the other field name by altering the index properties of the input properties and then
            # by joining them with '__'.
            field_name = '__'.join(input_properties[:-1] + ['1' if input_properties[2] == '0' else '0'])

            # extract the other value form the form's cleaned data
            radius_value = search_form['form'].cleaned_data.get(field_name) \
                if search_form['form'].cleaned_data.get(field_name) else 0

            # converting the value based on the input type
            if search_input.field_type == SearchInput.INT:
                radius_value_adjusted = int(radius_value)
            elif search_input.field_type == SearchInput.FLOAT:
                radius_value_adjusted = float(radius_value)
            else:
                radius_value_adjusted = radius_value

            # re-adjust the value
            value_adjusted += radius_value_adjusted * (-1 if input_properties[2] == '0' else 1)

        # find the operator and field operators based on the input type, index and dependent value
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
        """
        Lists a database search parameter, i.e., query parts for a particular user input.
        :param key: string variable name
        :param value:
        :param search_form:
        :return:
        """

        # splitting the key to separate
        # 1. search_input_group__name
        # 2. name
        # 3. index
        input_properties = key.split('__')

        # get the search input from the database
        try:
            search_input = SearchInput.objects.get(
                search_input_group__name=input_properties[0],
                name=input_properties[1],
                active=True,
            )
        except SearchInput.DoesNotExist:
            return

        # update the database search parameter for this input parameters.
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
        """
        Sets up the ORDER BY and LIMIT clause based on user input. Currently, search parameter form only takes these
        two inputs from the user. Based on the information passed, these two query clauses are computed.
        :param cleaned_data: cleaned data of the search parameters form
        """

        order_by = 'ASC'

        for key, value in cleaned_data.items():

            if key == 'results_per_page':
                self.limit = value

            if key == 'descending':
                order_by = 'DESC' if value else 'ASC'

        self.search_parameter_order_by = self.search_parameter_order_by.format(order_by=order_by)
        self.search_parameter_limit = self.search_parameter_limit.format(limit=self.limit, offset=self.offset)

    def _process_query(self):
        """
        For each search form in the search forms it decides whether they are processed uniquely (for search parameter
        form) or they are to be processed generally (for dynamic forms)
        """

        for search_form in self.search_forms:

            form = search_form.get('form')
            cleaned_data = form.cleaned_data

            # handling search parameter form, basically sets the
            # 1. ORDER BY clause
            # 2. LIMIT clause
            if type(form) is SearchParameterForm:
                self._process_search_parameters(cleaned_data)

            # handling database search forms (dynamic forms)
            if type(form) is SearchForm:
                for key, value in cleaned_data.items():
                    if value == '' or value is None:
                        continue

                    self._enlist_database_search_parameter(key, value, search_form)

    def get_query(self):
        """
        Function that is called from outside to get the query and its clauses
        :return: query string, values, order by clause, limit, offset, display headers
        """
        return \
            self.query, \
            self.query_values, \
            self.search_parameter_order_by, \
            self.limit, \
            self.offset, \
            self.display_headers

    def __init__(self, search_forms, form_type):
        """
        Initializes the class variables and then if the search forms are valid, processes and generates query.
        :param search_forms: Search forms that are passed.
        :param form_type: string to define the type of search forms. Ex: 'observation' or 'processing'.
            If this is extended then more checking will be required.
        """
        self.search_forms = search_forms

        # to store the query
        self.query = None

        # to store the query for counting total
        self.query_count = None

        # to render the query with values, should be in order
        self.query_values = []

        # limit for the query
        self.limit = 100

        # offset for the query
        self.offset = 0

        # stores the list of conditions for a search based on an input. Ex: necessary parameters to form
        # 'count(a.b) > 10' is stored as a dictionary format.
        self.database_search_parameters = []

        # display headers to be rendered in the UI.
        self.display_headers = []

        # constructing the initial ORDER BY clause based on the form type
        if form_type == 'observation':
            self.search_parameter_order_by = ' ORDER BY starttime {order_by}'
        else:
            self.search_parameter_order_by = ' ORDER BY job_id {order_by}'

        # setting up the search parameter LIMIT and OFFSET clause
        self.search_parameter_limit = ' LIMIT {limit} OFFSET {offset}'

        # if forms are valid proceed to process and generate query
        # otherwise, raise an error.
        if check_forms_validity(search_forms):
            self._process_query()
            self._generate_query(form_type)
        else:
            raise ValidationError('Invalid input parameters')
