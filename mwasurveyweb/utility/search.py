"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.core.exceptions import EmptyResultSet

from ..models import (
    SearchInput,
)


class SearchResults(object):

    def list_all(self):
        pass

    def __init__(self, search_forms):
        pass
