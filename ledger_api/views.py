import json

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from ledger_api.decorators import staff_required


class LoginRequiredMixin(object):
    """
    Adds login requirement.
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class StaffRequiredMixin(object):
    """
    Adds is_staff requirement.
    """

    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(*args, **kwargs)


class BackOfficeBaseMixin(LoginRequiredMixin, StaffRequiredMixin):
    """
    Base mixin for backoffice.
    """

    pass


class Backoffice(BackOfficeBaseMixin, TemplateView):
    """
    Backoffice angular app.
    """

    template_name = "backoffice/index.html"

    def get_context_data(self, **kwargs):
        """
        Updates and returns the context.
        """
        context = super(Backoffice, self).get_context_data(**kwargs)

        angular_app_variables = {
            "userName": str(self.request.user),
            "baseUrl": "".join(["https://", self.request.get_host()]),
        }

        context.update({"appVariables": json.dumps(angular_app_variables)})

        return context
