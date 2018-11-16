from django.db.models import Q
from django.urls import reverse

from .models import (
    SearchPage,
    SearchPageInputGroup,
    SearchInput,
)


def search_menu(request):
    input_groups = SearchInput.objects.values('search_input_group') \
        .filter(Q(active=True), ) \
        .distinct()

    search_pages = SearchPageInputGroup.objects.values('search_page') \
        .filter(Q(search_input_group__in=input_groups), Q(active=True), ) \
        .distinct()\
        .order_by('search_page__display_order')

    menu = []

    for search_page_dict in search_pages:
        search_page = SearchPage.objects.get(pk=search_page_dict.get('search_page'))
        menu.append(dict(
            link=reverse('search_' + search_page.name),
            display='Search ' + search_page.display_name,
        ))

    return {
        'SEARCH_MENU': menu,
    }
