from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from ...utility.utils import get_page_type
from ...utility.entity import Entity


@login_required
def view(request, object_id=None):

    # finding the type of the object
    object_type = get_page_type(request.path_info)

    entity = Entity(object_type=object_type, object_id=object_id)

    return render(
        request,
        "mwasurveyweb/view/view.html",
        {
            'search_forms': None,
            'object_type': object_type,
            'entity': entity,
        }
    )
