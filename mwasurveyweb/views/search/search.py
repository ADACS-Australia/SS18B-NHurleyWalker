"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

import pickle
import codecs
import re

from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from ...utility.paginator import Paginator
from ...forms.search_parameter import SearchParameterForm
from ...forms.search import SearchForm
from ...utility.search import SearchQuery
from ...utility.utils import (
    get_search_results,
    get_page_type,
    update_display_headers_order_by,
    get_order_by_parts,
)
from ...models import (
    SearchInputGroup,
    SearchInput,
    SearchPageInputGroup,
)


def set_session_search_attributes(request, query, query_values, display_headers, order_by, limit):
    """
    Sets up search attributes in the session
    :param request: django request object
    :param query: string representation of query
    :param query_values: list of values to render the query
    :param display_headers: list of search result display headers
    :param order_by: string representing the order by clause
    :param limit: limit clause
    """
    request.session['query'] = query
    request.session['query_values'] = codecs.encode(pickle.dumps(query_values), "base64").decode()
    request.session['display_headers'] = codecs.encode(pickle.dumps(display_headers), "base64").decode()
    request.session['order_by'] = order_by
    request.session['limit'] = limit


def reset_session_search_attributes(request):
    """
    Resets the session to None.
    :param request: django request object
    """
    request.session['query'] = None
    request.session['query_values'] = None
    request.session['display_headers'] = None
    request.session['order_by'] = None
    request.session['limit'] = None


def get_search_attributes_from_session(request):
    """
    Retrieve the search attributes from the session and returns them.
    :param request: django request attributes
    :return: search attributes stored in the session
    """
    query = request.session['query']
    query_values = pickle.loads(codecs.decode(request.session['query_values'].encode(), "base64"))
    display_headers = pickle.loads(codecs.decode(request.session['display_headers'].encode(), "base64"))
    order_by = request.session['order_by']
    limit = request.session['limit']

    return query, query_values, display_headers, order_by, limit


def build_search_forms(request, form_type):
    """
    Builds the search forms based on the form type and request data if exists. For input fields, apart from the search
    parameter form which is statically defined, this method queries the database and then uses dynamic form to build
    forms.
    :param request: django request object
    :param form_type: string defining the type of the form
    :return: list containing search forms
    """

    # generating search forms
    search_forms = [
        dict({
            'title': 'Search Parameters',
            'description': '',
            'form': SearchParameterForm(
                request.POST,
                name='search_parameter',
            ) if request.method == 'POST' else SearchParameterForm(
                name='search_parameter',
            ),
        }),
    ]

    # finding search input groups
    input_groups = SearchInputGroup.objects.filter(Q(active=True), ) \
        .order_by('display_order')

    for input_group in input_groups:

        # checking whether active search page input group is there for this input group.
        if not SearchPageInputGroup.objects.filter(
                search_page__name=form_type,
                search_input_group=input_group,
                active=True,
        ) \
                .exists():
            continue

        # checking whether any search input exists for the search input group
        if not SearchInput.objects.filter(active=True, search_input_group=input_group).exists():
            continue

        # building up form for the input group and then appending in the search forms list.
        search_forms.append(
            dict({
                'title': input_group.display_name,
                'description': input_group.description,
                'form': SearchForm(
                    request.POST,
                    name=input_group.name,
                ) if request.method == 'POST' else SearchForm(
                    name=input_group.name,
                ),
            })
        )

    return search_forms


@login_required
def search(request):
    """
    Render the search view. Arguably the most important view of the project. For post request, it returns the search
    results and sets the query parts in session so that these can be used later without going through the whole process
    again. For get request, there must be a query set which then is used to search, otherwise, it just builds the forms
    and displays those in the UI.
    :param request: Django request object.
    :return: Rendered template, either the search form or the result form
    """

    # getting the form type
    form_type = get_page_type(request.path_info)

    # If the request is get, there are 3 possibilities at this moment:
    # 1. pagination,
    # 2. sorting, and
    # 3. new form
    if request.method == 'GET':

        # checking for pagination to happen
        try:
            page = int(request.GET.get('page', None))

            # manually typing wrong page number will be barred.
            if page <= 0:
                return redirect(reverse('search_' + form_type) + '?page=1')
        except (TypeError, ValueError):
            page = None

        # checking whether the request is for sorting
        sort = request.GET.get('sort', None)

        # handling pagination here
        if page:

            try:

                # retrieve the previous query information that was stored in the session
                query, query_values, display_headers, order_by, limit = get_search_attributes_from_session(request)

                # changing the offset to adjust the query
                offset = (page - 1) * int(limit)
                pattern = ' OFFSET \d+'
                replace_with = ' OFFSET {}'.format(str(offset))

                # formulating new query with new offset
                query = re.sub(pattern, replace_with, query)

                # retrieving search results with new query
                search_results = list(get_search_results(query, query_values))[0]

                # extracting total number of results from the results
                try:
                    total = search_results[0][-1]
                except IndexError:
                    total = 0

                # getting the paginator
                paginator = Paginator(start_index=offset + 1, total=total, per_page=limit)

                return render(
                    request,
                    "mwasurveyweb/search/search.html",
                    {
                        'search_forms': None,
                        'search_results': search_results,
                        'display_headers': display_headers,
                        'paginator': paginator,
                        'view_page_link': 'view_' + form_type,
                    }
                )
            except (KeyError, AttributeError):
                reset_session_search_attributes(request)

        # handling sorting here
        elif sort:

            # new order by clause with default direction to to be ASC
            order_by_new = ' ORDER BY {field_name} {order_by_direction}'
            direction = 'ASC'

            # retrieve the previous query information that was stored in the session
            query, query_values, display_headers, order_by, limit = get_search_attributes_from_session(request)

            # analysing order by clause
            order_by_field, order_by_direction = get_order_by_parts(order_by)

            # if query is ordered by the same field and same direction, we just need to alter the direction
            if order_by_field == sort and order_by_direction == direction:
                direction = 'DESC'

            # formatting the oder by string
            order_by_new = order_by_new.format(
                field_name=sort,
                order_by_direction=direction,
            )

            # updating the query and display headers
            query = query.replace(order_by, order_by_new)
            update_display_headers_order_by(display_headers, order_by_new)

            # updating the session
            set_session_search_attributes(request, query, query_values, display_headers, order_by_new, limit)

            search_results = list(get_search_results(query, query_values))[0]

            try:
                total = search_results[0][-1]
            except IndexError:
                total = 0

            paginator = Paginator(start_index=1, total=total, per_page=limit)

            return render(
                request,
                "mwasurveyweb/search/search.html",
                {
                    'search_forms': None,
                    'search_results': search_results,
                    'display_headers': display_headers,
                    'paginator': paginator,
                    'view_page_link': 'view_' + form_type,
                }
            )

        else:
            reset_session_search_attributes(request)

    # building the forms
    search_forms = build_search_forms(request, form_type)

    # dealing with search results
    search_results = None
    paginator = None
    display_headers = None

    if request.method == 'POST':

        try:
            # building up search query
            search_query = SearchQuery(search_forms, form_type)
            query, query_values, order_by, limit, offset, display_headers = search_query.get_query()
            update_display_headers_order_by(display_headers, order_by)

            # update the session with the new query
            set_session_search_attributes(request, query, query_values, display_headers, order_by, limit)
        except ValidationError:
            # if form validation errors, setting everything to None
            query = None
            query_values = None
            limit = None
            offset = None

        # if there is a query, search result need to fetch, and search forms are voided, this would be checked in the UI
        if query:
            search_forms = None
            search_results = list(get_search_results(query, query_values))[0]

            try:
                total = search_results[0][-1]
            except IndexError:
                total = 0

            # paginator class for pagination
            paginator = Paginator(start_index=offset + 1, total=total, per_page=limit)

    return render(
        request,
        "mwasurveyweb/search/search.html",
        {
            'search_forms': search_forms,
            'search_results': search_results,
            'display_headers': display_headers,
            'paginator': paginator,
            'view_page_link': 'view_' + form_type,
        }
    )
