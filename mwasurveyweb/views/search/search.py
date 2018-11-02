"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ...forms.search import SearchForm

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

    search_results = None
    search_forms = []

    if request.method == 'POST':
        search_form = None
        search_results = None
    else:

        input_groups = SearchInputGroup.objects.filter(active=True)\
            .order_by('display_order')

        for input_group in input_groups:

            if not SearchInput.objects.filter(active=True, search_input_group=input_group).exists():
                continue

            search_forms.append(
                dict({
                    'title': input_group.display_name,
                    'description': input_group.description,
                    'form': SearchForm(name=input_group.name),
                })
            )

    return render(
        request,
        "mwasurveyweb/search/search.html",
        {
            'search_forms': search_forms,
            'search_results': search_results,
        }
    )
