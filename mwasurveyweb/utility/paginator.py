"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

import math


class Paginator(object):
    """
    Paginator class to facilitate pagination. This is doing something similar to Django pagination. However, we required
    to write a new one because Django pagination is available for django models. The GLEAM-X database is not modelled in
    this project. As a result, the necessity to have this class evolved.
    """

    def __init__(self, start_index, total, per_page):
        self.start_index = start_index
        self.total = total
        self.end_index = self.start_index - 1 + per_page

        # update for last page
        if self.total < self.end_index:
            self.end_index = self.total

        self.has_next = False
        self.has_previous = False

        if start_index > 1:
            self.has_previous = True

        if start_index + per_page < total:
            self.has_next = True

        self.num_pages = int(math.ceil(total / per_page))

        self.page_range = range(1, self.num_pages + 1)

        self.current_page = int(math.ceil(start_index / per_page))

        self.previous_page_number = 1
        self.next_page_number = self.num_pages

        if self.current_page - 1 > self.previous_page_number:
            self.previous_page_number = self.current_page - 1

        if self.current_page + 1 < self.next_page_number:
            self.next_page_number = self.current_page + 1
