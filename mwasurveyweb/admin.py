"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.contrib import admin

from .models import (
    SearchPage,
    SearchInputGroup,
    SearchInput,
    SearchInputOption,
    SearchPageInputGroup,
    SearchPageDisplayColumn,
    Colour,
    SkyPlotsConfiguration,
)


@admin.register(SearchPage)
class SearchPage(admin.ModelAdmin):
    list_display = (
        'display_name',
        'display_order',
        'active',
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
        'input_type',
        'initial_value',
        'placeholder',
        'required',
        'display_order',
        'active',
    )


@admin.register(SearchInputOption)
class SearchInputOption(admin.ModelAdmin):
    list_display = (
        'display_name',
        'search_input',
        'display_order',
        'active',
    )


@admin.register(SearchPageInputGroup)
class SearchPageInputGroup(admin.ModelAdmin):
    list_display = (
        'search_page',
        'search_input_group',
        'active',
    )


@admin.register(SearchPageDisplayColumn)
class SearchPageDisplayColumn(admin.ModelAdmin):
    list_display = (
        'search_page',
        'table_name',
        'field_name',
        'display_order',
        'active',
    )


@admin.register(Colour)
class Colour(admin.ModelAdmin):
    list_display = (
        'name',
        'code',
    )


@admin.register(SkyPlotsConfiguration)
class SkyPlotsConfiguration(admin.ModelAdmin):
    list_display = (
        'observation_status',
        'colour',
    )
