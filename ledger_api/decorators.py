from django.contrib import messages
from django.contrib.auth.views import logout_then_login
from django.urls import reverse
from functools import wraps


def staff_required(func):
    @wraps(func)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "Insuficiant user permisions!")
            return logout_then_login(request, reverse("login"))
        return func(request, *args, **kwargs)

    return wrapped
