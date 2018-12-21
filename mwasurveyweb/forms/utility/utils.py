"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from collections import OrderedDict

from ...constants import *
from ..dynamic import field as dynamic_field

from ...models import (
    SearchInput,
    SearchInputOption,
)


def get_choices_for_input(search_input):
    choices = []

    if not search_input.required:
        choices.append(
            ['', 'None'],
        )

    options = SearchInputOption.objects.filter(search_input=search_input)

    for option in options:
        choices.append([option.name, option.display_name])

    return choices


def get_fields(search_input):
    fields = []

    if search_input.input_type == TEXT:
        input_properties = dict()
        input_properties.update({
            'label': '',
            'type': dynamic_field.TEXT,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted,
        })
        fields.append(input_properties)

    elif search_input.input_type == NUMBER:
        input_properties = dict()
        input_properties.update({
            'label': '',
            'type': dynamic_field.INTEGER,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted,
        })
        fields.append(input_properties)

    elif search_input.input_type == MAX_NUMBER:
        input_properties = dict()
        input_properties.update({
            'label': '',
            'type': dynamic_field.INTEGER,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted,
        })
        fields.append(input_properties)

    elif search_input.input_type == MAX_ABSOLUTE_NUMBER:
        input_properties = dict()
        input_properties.update({
            'label': '',
            'type': dynamic_field.POSITIVE_INTEGER,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted,
        })
        fields.append(input_properties)

    elif search_input.input_type == CHECKBOX:
        input_properties = dict()
        input_properties.update({
            'label': '',
            'type': dynamic_field.CHECKBOX,
            'initial': search_input.initial_value_adjusted,
            'required': search_input.required,
        })
        fields.append(input_properties)

    elif search_input.input_type == SELECT:
        input_properties = dict()
        input_properties.update({
            'label': '',
            'type': dynamic_field.SELECT,
            'initial': search_input.initial_value_adjusted,
            'choices': get_choices_for_input(search_input),
            'required': search_input.required,
        })
        fields.append(input_properties)

    elif search_input.input_type == RANGE:
        input_properties_min = dict()
        input_properties_min.update({
            'label': 'Min',
            'type': dynamic_field.FLOAT,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted[0],
        })
        fields.append(input_properties_min)

        input_properties_max = dict()
        input_properties_max.update({
            'label': 'Max',
            'type': dynamic_field.FLOAT,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted[1],
        })
        fields.append(input_properties_max)

    elif search_input.input_type == RADIUS:
        input_properties_position = dict()
        input_properties_position.update({
            'label': 'Position',
            'type': dynamic_field.FLOAT,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted[0],
        })
        fields.append(input_properties_position)

        input_properties_plus_minus = dict()
        input_properties_plus_minus.update({
            'label': '+/-',
            'type': dynamic_field.POSITIVE_FLOAT,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted[1],
        })
        fields.append(input_properties_plus_minus)

    elif search_input.input_type in [DATE_GPS, DATE_UNIX, ]:
        input_properties = dict()
        input_properties.update({
            'label': '',
            'type': dynamic_field.DATE,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted,
        })
        fields.append(input_properties)

    elif search_input.input_type in [DATE_GPS_RANGE, DATE_UNIX_RANGE, ]:
        input_properties_min = dict()
        input_properties_min.update({
            'label': 'From',
            'type': dynamic_field.DATE,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted[0],
        })
        fields.append(input_properties_min)

        input_properties_max = dict()
        input_properties_max.update({
            'label': 'To',
            'type': dynamic_field.DATE,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted[1],
        })
        fields.append(input_properties_max)

    return fields


def get_field_properties(group_name):
    """
    Creates a Ordered Dictionary of field properties
    :return: Ordered Dictionary for fieldsets, Ordered Dictionary for field properties
    """
    field_properties = OrderedDict()
    fieldsets = OrderedDict()

    search_inputs = SearchInput.objects.filter(active=True, search_input_group__name=group_name) \
        .order_by('display_order')

    for search_input in search_inputs:
        fields = get_fields(search_input)

        # fieldsets fields
        fieldsets_fields = []

        for index, field in enumerate(fields):
            field_name = '{group_name}__{input_name}__{number}'.format(
                group_name=group_name,
                input_name=search_input.name,
                number=str(index),
            )

            field_properties.update({
                field_name: field,
            })

            fieldsets_fields.append(field_name)

        fieldsets.update({
            search_input.name: dict({
                'title': search_input.display_name,
                'fields': fieldsets_fields,
            })
        })

    # returning fieldsets and field properties
    return fieldsets, field_properties
