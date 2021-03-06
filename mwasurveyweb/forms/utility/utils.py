"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from collections import OrderedDict

from ... import constants
from ..dynamic import field as dynamic_field

from ...models import (
    SearchInput,
    SearchInputOption,
)


def get_choices_for_input(search_input):
    """
    Lists the choices for a search input. This is mainly used for select box and radios.
    :param search_input: search input object
    :return: list of choices.
    """

    choices = []

    # if search_input is not required there should be an option to leave it empty.
    # therefore the first input would be '' (empty string) with display 'None'
    if not search_input.required:
        choices.append(
            ['', 'None'],
        )

    # finding the options for the search input
    options = SearchInputOption.objects.filter(search_input=search_input)

    # appending the options to the list
    for option in options:
        choices.append([option.name, option.display_name])

    return choices


def get_fields(search_input):
    """
    Forms the field properties for a search input based on the input type and properties stored in the database.
    For some types it returns a list with only one field for which the label is empty. Because it takes the label of
    its fieldsets while rendering. For others, it returns a list of multiple fields, where each of them can have own
    label. Each of them also gets their corresponding initial value and help texts set up.
    :param search_input: instance of search input
    :return: a list of fields for that search input
    """
    fields = []

    if search_input.input_type == constants.TEXT:
        input_properties = dict()
        input_properties.update({
            'label': '',
            'type': dynamic_field.TEXT,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted,
            'help_text': search_input.help_text_adjusted,
        })
        fields.append(input_properties)

    elif search_input.input_type == constants.NUMBER:
        input_properties = dict()
        input_properties.update({
            'label': '',
            'type': dynamic_field.INTEGER,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted,
            'help_text': search_input.help_text_adjusted,
        })
        fields.append(input_properties)

    elif search_input.input_type == constants.MAX_NUMBER:
        input_properties = dict()
        input_properties.update({
            'label': '',
            'type': dynamic_field.INTEGER,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted,
            'help_text': search_input.help_text_adjusted,
        })
        fields.append(input_properties)

    elif search_input.input_type == constants.MAX_ABSOLUTE_NUMBER:
        input_properties = dict()
        input_properties.update({
            'label': '',
            'type': dynamic_field.POSITIVE_INTEGER,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted,
            'help_text': search_input.help_text_adjusted,
        })
        fields.append(input_properties)

    elif search_input.input_type == constants.CHECKBOX:
        input_properties = dict()
        input_properties.update({
            'label': '',
            'type': dynamic_field.CHECKBOX,
            'initial': search_input.initial_value_adjusted,
            'required': search_input.required,
            'help_text': search_input.help_text_adjusted,
        })
        fields.append(input_properties)

    elif search_input.input_type == constants.SELECT:
        input_properties = dict()
        input_properties.update({
            'label': '',
            'type': dynamic_field.SELECT,
            'initial': search_input.initial_value_adjusted,
            'choices': get_choices_for_input(search_input),
            'required': search_input.required,
            'help_text': search_input.help_text_adjusted,
        })
        fields.append(input_properties)

    elif search_input.input_type == constants.RANGE:
        input_properties_min = dict()
        input_properties_min.update({
            'label': 'Min',
            'type': dynamic_field.FLOAT,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted[0],
            'help_text': search_input.help_text_adjusted[0],
        })
        fields.append(input_properties_min)

        input_properties_max = dict()
        input_properties_max.update({
            'label': 'Max',
            'type': dynamic_field.FLOAT,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted[1],
            'help_text': search_input.help_text_adjusted[1],
        })
        fields.append(input_properties_max)

    elif search_input.input_type == constants.RANGE_INT:
        input_properties_min = dict()
        input_properties_min.update({
            'label': 'Min',
            'type': dynamic_field.INTEGER,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted[0],
            'help_text': search_input.help_text_adjusted[0],
        })
        fields.append(input_properties_min)

        input_properties_max = dict()
        input_properties_max.update({
            'label': 'Max',
            'type': dynamic_field.INTEGER,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted[1],
            'help_text': search_input.help_text_adjusted[1],
        })
        fields.append(input_properties_max)

    elif search_input.input_type == constants.RANGE_NON_NEG_INT:
        input_properties_min = dict()
        input_properties_min.update({
            'label': 'Min',
            'type': dynamic_field.INTEGER_NON_NEGATIVE,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted[0],
            'help_text': search_input.help_text_adjusted[0],
        })
        fields.append(input_properties_min)

        input_properties_max = dict()
        input_properties_max.update({
            'label': 'Max',
            'type': dynamic_field.INTEGER_NON_NEGATIVE,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted[1],
            'help_text': search_input.help_text_adjusted[1],
        })
        fields.append(input_properties_max)

    elif search_input.input_type == constants.RADIUS:
        input_properties_position = dict()
        input_properties_position.update({
            'label': 'Position',
            'type': dynamic_field.FLOAT,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted[0],
            'help_text': search_input.help_text_adjusted[0],
        })
        fields.append(input_properties_position)

        input_properties_plus_minus = dict()
        input_properties_plus_minus.update({
            'label': '+/-',
            'type': dynamic_field.POSITIVE_FLOAT,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted[1],
            'help_text': search_input.help_text_adjusted[1],
        })
        fields.append(input_properties_plus_minus)

    elif search_input.input_type in [constants.DATE_GPS, constants.DATE_UNIX, ]:
        input_properties = dict()
        input_properties.update({
            'label': '',
            'type': dynamic_field.DATE,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted,
            'help_text': search_input.help_text_adjusted,
        })
        fields.append(input_properties)

    elif search_input.input_type in [constants.DATE_GPS_RANGE, constants.DATE_UNIX_RANGE, ]:
        input_properties_min = dict()
        input_properties_min.update({
            'label': 'From',
            'type': dynamic_field.DATE,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted[0],
            'help_text': search_input.help_text_adjusted[0],
        })
        fields.append(input_properties_min)

        input_properties_max = dict()
        input_properties_max.update({
            'label': 'To',
            'type': dynamic_field.DATE,
            'required': search_input.required,
            'placeholder': search_input.placeholder,
            'initial': search_input.initial_value_adjusted[1],
            'help_text': search_input.help_text_adjusted[1],
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

    # finds the search inputs that belong to the group and are currently active.
    search_inputs = SearchInput.objects.filter(active=True, search_input_group__name=group_name) \
        .order_by('display_order')

    for search_input in search_inputs:

        # get the fields for the search input. See function definition for details.
        fields = get_fields(search_input)

        # fieldsets fields
        fieldsets_fields = []

        # for each field in the fields generating a name and updating the field_properties by that name
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

        # finally updating the fieldsets
        fieldsets.update({
            search_input.name: dict({
                'title': search_input.display_name,
                'fields': fieldsets_fields,
            })
        })

    # returning fieldsets and field properties
    return fieldsets, field_properties
