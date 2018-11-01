"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import common
from .views.search import search


urlpatterns = [
    path('', common.index, name='index'),
    path('about/', common.about, name='about'),
    path('search/', login_required(search.search), name='search'),
]
