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
    request.session['query'] = query
    request.session['query_values'] = codecs.encode(pickle.dumps(query_values), "base64").decode()
    request.session['display_headers'] = codecs.encode(pickle.dumps(display_headers), "base64").decode()
    request.session['order_by'] = order_by
    request.session['limit'] = limit


def reset_session_search_attributes(request):
    request.session['query'] = None
    request.session['query_values'] = None
    request.session['display_headers'] = None
    request.session['order_by'] = None
    request.session['limit'] = None


def get_search_attributes_from_session(request):
    query = request.session['query']
    query_values = pickle.loads(codecs.decode(request.session['query_values'].encode(), "base64"))
    display_headers = pickle.loads(codecs.decode(request.session['display_headers'].encode(), "base64"))
    order_by = request.session['order_by']
    limit = request.session['limit']

    return query, query_values, display_headers, order_by, limit


def build_search_forms(request, form_type):
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

    input_groups = SearchInputGroup.objects.filter(Q(active=True), ) \
        .order_by('display_order')

    for input_group in input_groups:

        if not SearchPageInputGroup.objects.filter(
                search_page__name=form_type,
                search_input_group=input_group,
                active=True,
        ) \
                .exists():
            continue

        if not SearchInput.objects.filter(active=True, search_input_group=input_group).exists():
            continue

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
    Render the search view.
    :param request: Django request object.
    :return: Rendered template
    """

    form_type = get_page_type(request.path_info)

    if request.method == 'GET':

        try:
            page = int(request.GET.get('page', None))
        except (TypeError, ValueError):
            page = None

        sort = request.GET.get('sort', None)

        if page:
            # handling pagination here

            if page < 1:
                return redirect(reverse('search_' + form_type) + '?page=1')

            try:
                query, query_values, display_headers, order_by, limit = get_search_attributes_from_session(request)
                offset = (page - 1) * int(limit)

                pattern = ' OFFSET \d+'
                replace_with = ' OFFSET {}'.format(str(offset))

                query = re.sub(pattern, replace_with, query)

                search_results = list(get_search_results(query, query_values))[0]

                try:
                    total = search_results[0][-1]
                except IndexError:
                    total = 0

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

        elif sort:

            # handling sorting here

            order_by_new = ' ORDER BY {field_name} {order_by_direction}'

            direction = 'ASC'

            query, query_values, display_headers, order_by, limit = get_search_attributes_from_session(request)

            order_by_field, order_by_direction = get_order_by_parts(order_by)

            if order_by_field == sort and order_by_direction == direction:
                direction = 'DESC'

            order_by_new = order_by_new.format(
                field_name=sort,
                order_by_direction=direction,
            )

            query = query.replace(order_by, order_by_new)
            update_display_headers_order_by(display_headers, order_by_new)

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

    search_forms = build_search_forms(request, form_type)

    # dealing with search results
    search_results = None
    paginator = None
    display_headers = None

    if request.method == 'POST':

        try:
            search_query = SearchQuery(search_forms, form_type)
            query, query_values, order_by, limit, offset, display_headers = search_query.get_query()
            update_display_headers_order_by(display_headers, order_by)
            set_session_search_attributes(request, query, query_values, display_headers, order_by, limit)
        except ValidationError:
            query = None
            query_values = None
            limit = None
            offset = None

        if query:
            search_forms = None
            search_results = list(get_search_results(query, query_values))[0]

            try:
                total = search_results[0][-1]
            except IndexError:
                total = 0

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
