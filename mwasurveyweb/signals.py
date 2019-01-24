"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

import os

from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings

from .models import SkyPlot


@receiver(post_delete, sender=SkyPlot, dispatch_uid='delete_image_file')
def delete_image_file(instance, **kwargs):
    """
    Signal to delete image file physically if the skyplot is removed
    :param instance: instance of Skyplot model.
    :param kwargs: keyword arguments.
    :return: Nothing
    """
    try:
        os.remove(os.path.join(settings.BASE_DIR,
                               '..',
                               'static/images/skyplots/',
                               '{}'.format(instance.name)
                               )
                  )
    except FileNotFoundError:
        pass
