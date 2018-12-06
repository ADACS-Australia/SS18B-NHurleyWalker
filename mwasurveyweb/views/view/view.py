from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ...utility.utils import get_page_type
from ...utility.observation import Observation
from ...utility.processing import Processing


@login_required
def view(request, object_id=None):

    # finding the type of the object
    object_type = get_page_type(request.path_info)

    if object_type == 'observation':

        observation = Observation(observation_id=object_id)

        return render(
            request,
            "mwasurveyweb/view/observation.html",
            {
                'observation': observation,
            }
        )

    elif object_type == 'processing':
        processing = Processing(processing_id=object_id)

        return render(
            request,
            "mwasurveyweb/view/processing.html",
            {
                'processing': processing,
            }
        )
