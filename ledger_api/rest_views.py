import account.models as account_models
import base.models as base_models
import datetime
import django_filters
import ledger_api.serializers as serializers
import logging

from account.constants.account import BANK_ACCOUNT
from account.constants.account import GENERAL_ACCOUNT
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from ledger_api.controllers.dashboard_controller import DashboardController
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

logger = logging.getLogger(
    getattr(settings, "LOGGER_ROOT_NAME", "bank") + "." + __name__
)


class BankLineImportError(Exception):
    """
    Exception representing a BankLineImportError.
    """

    pass


class BaseFilterSet(django_filters.FilterSet):
    """
    Base filter set for all filters.
    """

    filter_overrides = {
        models.CharField: {
            "filter_class": django_filters.CharFilter,
            "extra": lambda f: {"lookup_type": "icontains"},
        },
        models.EmailField: {
            "filter_class": django_filters.CharFilter,
            "extra": lambda f: {"lookup_type": "icontains"},
        },
    }


class DashboardView(viewsets.ViewSet):
    """
    Dashboard view set.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        controller = DashboardController()
        data = {
            "display_months": controller.DISPLAY_MONTHS,
            "display_days": controller.DISPLAY_DAYS + 1,
            "active_weeks": controller.ACTIVE_WEEKS,
            "months_average": controller.MONTHS_AVERAGE,
            "total_users": controller.total_users(),
            "active_users": controller.active_users(),
            "online_users": controller.online_users(),
            "current_liability": str(controller.current_liability()),
            "user_sign_ups": controller.user_sign_ups(),
            "liability_balance": controller.liability_balance(),
            "deal_create_metrics": controller.deal_create_metrics(),
            "deal_states": controller.deal_states(),
            "avg_trans": controller.avg_trans(),
            "trans_duration": controller.trans_duration(),
            "trans_progress": controller.trans_progress(),
        }
        return Response(data)


class UsersViewSet(viewsets.ModelViewSet):
    """
    Users view set.
    """

    class UsersFilter(BaseFilterSet):
        class Meta:
            model = get_user_model()
            fields = ["username", "first_name", "last_name", "email"]

    queryset = get_user_model().objects.all().order_by("username")
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_class = UsersFilter


class ProfileViewSet(viewsets.ModelViewSet):
    """
    User profile view set.
    """

    queryset = base_models.UserProfile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "user"


class EntitiesViewSet(viewsets.ModelViewSet):
    """
    Entities view set.
    """

    class EntitiesFilter(BaseFilterSet):
        class Meta:
            model = base_models.Entity
            fields = ["name", "entity_no", "email", "entity_type"]

    queryset = base_models.Entity.objects.all().order_by("id")
    serializer_class = serializers.EntitySerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_class = EntitiesFilter


class EntitiesForUserViewSet(viewsets.ViewSet):
    """
    Entities for given user view set.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, pk=None):
        queryset = get_user_model().objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = serializers.EntitySerializer(
            user.entities.all(), many=True
        )
        return Response(serializer.data)


class UsersForEntityViewSet(viewsets.ViewSet):
    """
    Users for given entity view set.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, pk=None):
        queryset = base_models.Entity.objects.all()
        entity = get_object_or_404(queryset, pk=pk)
        serializer = serializers.UserSerializer(entity.users.all(), many=True)
        return Response(serializer.data)


class AccountViewSet(viewsets.ModelViewSet):
    """
    Traders account view set.
    """

    class TradersAccountFilter(BaseFilterSet):
        class Meta:
            model = account_models.Account
            fields = [
                "acc_no",
                "name",
                "accounting_type",
                "state",
                "debit",
                "credit",
                "pending_balance",
                "available_balance",
                "balance",
            ]

    queryset = account_models.Account.objects.all()
    lookup_field = "acc_no"
    serializer_class = serializers.AccountSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_class = TradersAccountFilter

    def get_queryset(self):
        queryset = super(AccountViewSet, self).get_queryset()
        ordering = self.request.query_params.get("ordering", None)
        if ordering:
            queryset.order_by(ordering)
        queryset.order_by("acc_no")
        return queryset

    def filter_queryset(self, queryset):
        queryset = super(AccountViewSet, self).filter_queryset(queryset)
        ordering = self.request.query_params.get("ordering", None)
        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset

    @detail_route()
    def statement(self, request, acc_no=None):
        account = get_object_or_404(account_models.Account, acc_no=acc_no)
        statement = account.account_entry_lines.all().order_by("-date_created")

        page = self.paginate_queryset(statement)
        if page is not None:
            serializer = serializers.JournalEntryLineSerializer(
                page, many=True
            )
            return self.get_paginated_response(serializer.data)

        serializer = serializers.JournalEntryLineSerializer(
            statement, many=True
        )
        return Response(serializer.data)


class AccountTradersViewSet(AccountViewSet):
    """
    Traders account view set.
    """

    vault_type = account_models.AccountType.objects.get(code="TRADERS")
    queryset = account_models.Account.objects.filter(internal_type=vault_type)


class AccountGeneralViewSet(AccountViewSet):
    """
    General account view set.
    """

    vault_type = account_models.AccountType.objects.get(code=GENERAL_ACCOUNT)
    queryset = account_models.Account.objects.filter(internal_type=vault_type)


class AccountBankViewSet(AccountViewSet):
    """
    Bank account view set.
    """

    vault_type = account_models.AccountType.objects.get(code=BANK_ACCOUNT)
    queryset = account_models.Account.objects.filter(internal_type=vault_type)


class JournalEntriesViewSet(viewsets.ModelViewSet):
    """
    Journal entries view set.
    """

    class JournalEntryFilter(BaseFilterSet):
        journal__name = django_filters.CharFilter(
            name="journal__name", lookup_type="icontains"
        )

        class Meta:
            model = account_models.JournalEntry
            fields = ["ref_no", "name", "journal__name", "state"]

    queryset = account_models.JournalEntry.objects.all().order_by(
        "-date_created"
    )
    lookup_field = "ref_no"
    serializer_class = serializers.JournalEntrySerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_class = JournalEntryFilter

    def filter_queryset(self, queryset):
        queryset = super(JournalEntriesViewSet, self).filter_queryset(queryset)
        date_created_gte = self.request.query_params.get(
            "date_created_gte", None
        )
        date_created_lte = self.request.query_params.get(
            "date_created_lte", None
        )
        if date_created_gte:
            queryset = queryset.filter(
                date_created__gte=datetime.datetime.strptime(
                    date_created_gte, "%Y-%m-%d"
                )
            )
        if date_created_lte:
            queryset = queryset.filter(
                date_created__lte=datetime.datetime.strptime(
                    date_created_lte, "%Y-%m-%d"
                )
            )

        ordering = self.request.query_params.get("ordering", None)
        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset

    @detail_route()
    def entry_lines(self, request, ref_no=None):
        entry = get_object_or_404(account_models.JournalEntry, ref_no=ref_no)
        lines = entry.entry_lines.all()
        serializer = serializers.JournalEntryLineSerializer(lines, many=True)
        return Response(serializer.data)
