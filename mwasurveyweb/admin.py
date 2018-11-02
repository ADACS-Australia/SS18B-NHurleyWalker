"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.contrib import admin

from .models import (
    SearchInputGroup,
    SearchInput,
)


@admin.register(SearchInputGroup)
class SearchInputGroup(admin.ModelAdmin):
    list_display = (
        'display_name',
        'description',
        'display_order',
        'active',
    )


@admin.register(SearchInput)
class SearchInput(admin.ModelAdmin):
    list_display = (
        'display_name',
        'search_input_group',
        'table_name',
        'field_name',
        'field_type',
        'initial_value',
        'placeholder',
        'required',
        'display_order',
        'active',
    )
