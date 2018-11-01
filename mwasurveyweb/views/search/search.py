"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def search(request):
    """
    Render the search view.
    :param request: Django request object.
    :return: Rendered template
    """

    search_results = None

    if request.method == 'POST':
        search_form = None
        search_results = None
    else:
        search_form = None

    return render(
        request,
        "mwasurveyweb/search/search.html",
        {
            'search_form': search_form,
            'search_results': search_results,
        }
    )
