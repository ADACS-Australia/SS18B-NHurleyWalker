"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

import logging
from collections import OrderedDict

from .dynamic.form import DynamicForm
from .dynamic import field

logger = logging.getLogger(__name__)

SEARCH_PARAMETER_FIELD_PROPERTIES = OrderedDict([
    ('results_per_page', {
        'type': field.POSITIVE_INTEGER,
        'label': '',
        'placeholder': '100',
        'initial': 100,
        'required': True,
    }),
    ('descending', {
        'type': field.CHECKBOX,
        'label': '',
        'initial': False,
        'required': False,
        'help_text': 'Check to sort initially in reverse order',
    }),
])


class SearchParameterForm(DynamicForm):
    """
    Defines the search form from the database
    """

    # An Ordered Dictionary to render the fields in order in the template
    fieldsets = OrderedDict(
        results_per_page=dict({
            'title': 'Results Per Page',
            'fields': ['results_per_page'],
        }),
        descending=dict({
            'title': 'Descending Order?',
            'fields': ['descending'],
        })
    )

    def __init__(self, *args, **kwargs):
        kwargs['name'] = kwargs.get('name', None)
        kwargs['field_properties'] = SEARCH_PARAMETER_FIELD_PROPERTIES

        self.fieldsets.update()

        super(SearchParameterForm, self).__init__(*args, **kwargs)
