"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Returns the object for that key from a dictionary.
    :param dictionary: A dictionary object
    :param key: Key to search for
    :return: Object that corresponds to the key in the dictionary
    """
    return dictionary.get(key, None)
