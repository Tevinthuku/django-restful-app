"""
utility functions that will
be used accross various files.
"""
from django.http import HttpResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


def resolve_response(data, status=200):
    """
        this function reduces boilerplate when it comes to 
        returning a response in a request, one thing that is easily
        forgotten is the content_type
    """
    return HttpResponse(data, content_type="application/json", status=status)


# validation functions
def check_for_whitespaces(data, checklist):
    """
        This function checks for whitespaces in the
        dict items that are provided
    """
    for key, value in data.items():
        if key in checklist and not value.strip():
            raise forms.ValidationError(
                '{} field cannot be left blank'.format(key))
    return True


class CSRFExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def is_json(data):
    """
        This function checks if the 
        data provided is valid json
    """
    try:
        json.loads(data)
        is_valid = True
    except ValueError:
        is_valid = False
    return is_valid
