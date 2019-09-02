"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django import template

from ..utility import get_absolute_site_url

register = template.Library()


@register.simple_tag(name='absolute_url', takes_context=True)
def absolute_url(context):
    return get_absolute_site_url(protocol=context['protocol'], site_name=context['site_name'])
