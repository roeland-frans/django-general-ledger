import account.models as account_models
import base.models as base_models
import re

from datetime import date
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


def validate_id_no(id_no):
    if not id_no:
        raise serializers.ValidationError(_("This field is required."))
    else:
        id_re = re.compile(
            r"^(?P<yy>\d\d)(?P<mm>\d\d)(?P<dd>\d\d)(?P<mid>\d{4})(?P<end>\d{3})"
        )
        id_no = id_no.strip().replace(" ", "").replace("-", "")
        match = re.match(id_re, id_no)
        error_msg = _("Invalid ID number, enter a valid SA ID number.")

        if not match:
            raise serializers.ValidationError(error_msg)
        g = match.groupdict()

        try:
            # The year 2000 is conveniently a leapyear.
            # This algorithm will break in xx00 years which aren't leap years
            # There is no way to guess the century of a ZA ID number
            d = date(int(g["yy"]) + 2000, int(g["mm"]), int(g["dd"]))
        except ValueError:
            raise serializers.ValidationError(error_msg)

    return id_no


class CurrencySerializer(serializers.ModelSerializer):
    """
    Serializer for currency.
    """

    class Meta:
        model = account_models.Currency
        fields = ("code", "name", "is_base", "current_rate", "date")
        read_only_fields = ("code", "name", "is_base", "current_rate", "date")


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for users.
    """

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "last_login",
            "is_superuser",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
        )
        read_only_fields = (
            "id",
            "last_login",
            "is_superuser",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "date_joined",
        )
        extra_kwargs = {"username": {"validators": [validate_email]}}


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profiles.
    """

    class Meta:
        model = base_models.UserProfile
        fields = (
            "id",
            "activation_key",
            "email_secondary",
            "mobile",
            "id_no",
            "passport_no",
            "passport_country",
            "dob",
            "call_count",
            "login_notifications",
            "sms_critical",
            "email_critical",
            "sms_other",
            "email_other",
            "avatar_thumbnail",
            "session_key",
            "locked",
            "user",
        )
        read_only_fields = (
            "activation_key",
            "email_secondary",
            "mobile",
            "dob",
            "call_count",
            "login_notifications",
            "sms_critical",
            "email_critical",
            "sms_other",
            "email_other",
            "avatar_thumbnail",
            "session_key",
            "locked",
            "user",
        )
        extra_kwargs = {"id_no": {"validators": [validate_id_no]}}


class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer for addresses.
    """

    class Meta:
        model = base_models.Address
        fields = ("address", "suburb", "city", "province", "code")
        read_only_fields = ("address", "suburb", "city", "province", "code")


class EntitySerializer(serializers.ModelSerializer):
    """
    Serializer for users.
    """

    physical_address = AddressSerializer()
    postal_address = AddressSerializer()

    class Meta:
        model = base_models.Entity
        fields = (
            "id",
            "entity_no",
            "entity_type",
            "name",
            "reg_no",
            "telephone",
            "fax",
            "email",
            "bank_verify_count",
            "physical_address",
            "postal_address",
            "current_bank_account",
            "users",
        )
        read_only_fields = (
            "id",
            "entity_no",
            "entity_type",
            "name",
            "reg_no",
            "telephone",
            "fax",
            "email",
            "bank_verify_count",
            "physical_address",
            "postal_address",
            "current_bank_account",
            "users",
        )


class BankSerializer(serializers.ModelSerializer):
    """
    Serializer for banks.
    """

    class Meta:
        model = base_models.Bank
        fields = (
            "name",
            "validated_name",
            "swift_code",
            "code",
            "eft_branch_code",
            "can_verify_accounts",
        )
        read_only_fields = (
            "name",
            "validated_name",
            "swift_code",
            "code",
            "eft_branch_code",
            "can_verify_accounts",
        )


class EntityBankAccountSerializer(serializers.ModelSerializer):
    """
    Serializer for entity bank accounts.
    """

    bank = BankSerializer()
    entity = EntitySerializer()

    class Meta:
        model = base_models.EntityBankAccount
        fields = (
            "acc_no",
            "entity",
            "bank_account_type",
            "state",
            "bank",
            "bank_name",
            "branch",
        )
        read_only_fields = (
            "acc_no",
            "entity",
            "bank_account_type",
            "state",
            "bank",
            "bank_name",
            "branch",
        )


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for accounts.
    """

    debit = serializers.SerializerMethodField()
    credit = serializers.SerializerMethodField()
    pending_balance = serializers.SerializerMethodField()
    available_balance = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()

    class Meta:
        model = account_models.Account
        fields = (
            "acc_no",
            "name",
            "accounting_type",
            "state",
            "debit",
            "credit",
            "pending_balance",
            "available_balance",
            "balance",
            "date_created",
            "last_activity",
        )
        read_only_fields = (
            "acc_no",
            "name",
            "accounting_type",
            "debit",
            "credit",
            "pending_balance",
            "available_balance",
            "balance",
            "date_created",
            "last_activity",
        )

    def get_debit(self, obj):
        return str(obj.debit)

    def get_credit(self, obj):
        return str(obj.credit)

    def get_pending_balance(self, obj):
        return str(obj.pending_balance)

    def get_available_balance(self, obj):
        return str(obj.available_balance)

    def get_balance(self, obj):
        return str(obj.balance)


class JournalEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for journal entries.
    """

    journal__name = serializers.SerializerMethodField()

    class Meta:
        model = account_models.JournalEntry
        fields = ("ref_no", "name", "date_created", "journal__name", "state")
        read_only_fields = (
            "ref_no",
            "name",
            "date_created",
            "journal__name",
            "state",
        )

    def get_journal__name(self, obj):
        return obj.journal.name


class JournalEntryLineSerializer(serializers.ModelSerializer):
    """
    Serializer for journal entry lines.
    """

    journal_entry = serializers.SerializerMethodField()
    debit = serializers.SerializerMethodField()
    credit = serializers.SerializerMethodField()
    account_balance = serializers.SerializerMethodField()
    account_name = serializers.SerializerMethodField()
    account_number = serializers.SerializerMethodField()

    class Meta:
        model = account_models.JournalEntryLine
        fields = (
            "pk",
            "date_created",
            "ref_no",
            "name",
            "journal_entry",
            "debit",
            "credit",
            "account_balance",
            "entity",
            "state",
            "account_name",
            "account_number",
        )
        read_only_fields = (
            "pk",
            "date_created",
            "ref_no",
            "name",
            "journal_entry",
            "debit",
            "credit",
            "account_balance",
            "entity",
            "state",
            "account_name",
            "account_number",
        )

    def get_journal_entry(self, obj):
        return str(obj.journal_entry.ref_no)

    def get_debit(self, obj):
        return str(obj.debit)

    def get_credit(self, obj):
        return str(obj.credit)

    def get_account_balance(self, obj):
        return str(obj.account_balance)

    def get_account_name(self, obj):
        return str(obj.account)

    def get_account_number(self, obj):
        return str(obj.account.acc_no)
