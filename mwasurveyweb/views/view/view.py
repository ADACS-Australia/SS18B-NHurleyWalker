"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ...utility.utils import get_page_type
from ...utility.observation import Observation
from ...utility.processing import Processing


@login_required
def view(request, object_id=None):
    """
    View to view a single observation or processing
    :param request: django request object
    :param object_id: id of processing or observation
    :return: rendered template
    """
    # finding the type of the object
    object_type = get_page_type(request.path_info)

    if object_type == 'observation':

        with Observation(observation_id=object_id) as observation:

            return render(
                request,
                "mwasurveyweb/view/observation.html",
                {
                    'observation': observation,
                }
            )

    elif object_type == 'processing':

        with Processing(processing_id=object_id) as processing:

            return render(
                request,
                "mwasurveyweb/view/processing.html",
                {
                    'processing': processing,
                }
            )
