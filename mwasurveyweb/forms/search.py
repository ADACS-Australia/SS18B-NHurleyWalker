"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

import logging

from .dynamic.form import DynamicForm
from .utility.utils import get_field_properties


logger = logging.getLogger(__name__)


class SearchForm(DynamicForm):
    """
    Defines the search form from the database
    """

    # An Ordered Dictionary to render the fields in order in the template
    fieldsets = None

    def __init__(self, *args, **kwargs):
        group_name = kwargs.get('name', None)
        fieldsets, field_properties = get_field_properties(group_name)

        self.fieldsets = fieldsets
        kwargs['field_properties'] = field_properties

        super(SearchForm, self).__init__(*args, **kwargs)
