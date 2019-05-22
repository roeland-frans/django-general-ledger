import json

from base.constants import SYSTEM_USERNAME
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from pycountry import subdivisions


def get_or_create_profile(user):
    try:
        return user.get_profile()
    except ObjectDoesNotExist:
        app_label, model_name = settings.AUTH_PROFILE_MODULE.split(".")
        model = models.get_model(app_label, model_name)
        return model.objects.get_or_create(user=user)[0]


def get_system_user():
    """
    This will return the system user.
    """
    try:
        system_user = get_user_model().objects.get(username=SYSTEM_USERNAME)
    except ObjectDoesNotExist:
        system_user = False
    return system_user


def generate_country_province_mapper():
    """
    Generates a country province mapper JSON dump that can be used by AngularJS
    to dynamically change province form field options based on country field
    value. This should not really be used in Python, helper to generate for
    static JS files.
    """
    mapper = {}
    for subdiv in subdivisions:
        if subdiv.country.alpha2 in mapper:
            mapper[subdiv.country.alpha2][subdiv.code] = subdiv.name
        else:
            mapper[subdiv.country.alpha2] = {subdiv.code: subdiv.name}

    print(json.dumps(mapper))
