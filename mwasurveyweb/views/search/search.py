"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.core.exceptions import EmptyResultSet
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ...forms.search_parameter import SearchParameterForm
from ...forms.search import SearchForm
from ...utility.search import SearchResults
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

    # generating search forms
    search_forms = [
        dict({
            'title': 'Search Parameters',
            'description': '',
            'form': SearchParameterForm(
                request.POST,
                name='search_parameter',
                prefix='search_parameter',
            ) if request.method == 'POST' else SearchParameterForm(
                name='search_parameter',
                prefix='search_parameter',
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
                    prefix=input_group.name,
                ) if request.method == 'POST' else SearchForm(
                    name=input_group.name,
                    prefix=input_group.name,
                ),
            })
        )

    # dealing with search results
    search_results = None

    if request.method == 'POST':
        try:
            search_results_object = SearchResults(search_forms)
            search_results = search_results_object.list_all()
        except EmptyResultSet:
            pass

    return render(
        request,
        "mwasurveyweb/search/search.html",
        {
            'search_forms': search_forms,
            'search_results': search_results,
        }
    )
