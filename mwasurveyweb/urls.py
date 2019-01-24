"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import common
from .views.search import search
from .views.view import view
from .models import SearchPage


search_urls = []

try:
    search_pages = SearchPage.objects.all()

    for search_page in search_pages:
        # search url
        search_urls.append(
            path(
                'search_' + search_page.name + '/',
                login_required(search.search),
                name='search_' + search_page.name,
            ),
        )

        # view single object url
        search_urls.append(
            path(
                'view_' + search_page.name + '/<object_id>/',
                login_required(view.view),
                name='view_' + search_page.name,
            ),
        )
except:
    pass

urlpatterns = [
    path('', common.index, name='index'),
    path('about/', common.about, name='about'),
]

urlpatterns += search_urls
