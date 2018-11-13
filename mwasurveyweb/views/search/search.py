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

from ...utility.Paginator import Paginator
from ...forms.search_parameter import SearchParameterForm
from ...forms.search import SearchForm
from ...utility.search import SearchQuery
from ...utility.utils import get_search_results
from ...models import (
    SearchInputGroup,
    SearchInput,
)


@login_required
def search(request):
    """
    Render the search view.
    :param request: Django request object.
    :return: Rendered template
    """

    if request.method == 'GET':

        try:
            page = int(request.GET.get('page', None))
        except (TypeError, ValueError):
            page = None

        if page:
            # pagination is happening

            if page < 1:
                return redirect(reverse('search') + '?page=1')

            try:
                query = request.session['query']
                query_values = pickle.loads(codecs.decode(request.session['query_values'].encode(), "base64"))
                limit = request.session['limit']
                offset = (page - 1) * int(limit)

                pattern = ' OFFSET \d+'
                replace_with = ' OFFSET {}'.format(str(offset))

                query = re.sub(pattern, replace_with, query)

                search_results = list(get_search_results(query, query_values))[0]

                try:
                    total = search_results[0]['total']
                except IndexError:
                    total = 0

                paginator = Paginator(start_index=offset + 1, total=total, per_page=limit)

                return render(
                    request,
                    "mwasurveyweb/search/search.html",
                    {
                        'search_forms': None,
                        'search_results': search_results,
                        'paginator': paginator,
                    }
                )
            except (KeyError, AttributeError):
                request.session['query'] = None
                request.session['query_values'] = None
                request.session['limit'] = None

        else:
            request.session['query'] = None
            request.session['query_values'] = None
            request.session['limit'] = None

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

    input_groups = SearchInputGroup.objects.filter(active=True) \
        .order_by('display_order')

    for input_group in input_groups:

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

    # dealing with search results
    search_results = None
    paginator = None

    if request.method == 'POST':

        try:
            search_query = SearchQuery(search_forms)
            query, query_values, limit, offset = search_query.get_query()
            request.session['query'] = query
            request.session['query_values'] = codecs.encode(pickle.dumps(query_values), "base64").decode()
            request.session['limit'] = limit
        except ValidationError:
            query = None
            query_values = None
            limit = None
            offset = None

        if query:
            search_forms = None
            search_results = list(get_search_results(query, query_values))[0]

            try:
                total = search_results[0]['total']
            except IndexError:
                total = 0

            paginator = Paginator(start_index=offset + 1, total=total, per_page=limit)

    return render(
        request,
        "mwasurveyweb/search/search.html",
        {
            'search_forms': search_forms,
            'search_results': search_results,
            'paginator': paginator,
        }
    )
