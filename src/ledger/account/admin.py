from account.models import Account
from account.models import AccountType
from account.models import Currency
from account.models import CurrencyRate
from account.models import Journal
from account.models import JournalEntry
from account.models import JournalEntryLine
from account.models import Reconcile
from django.contrib import admin


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "current_rate", "date", "is_base")


class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ("date_from", "currency", "rate")
    list_filter = ("currency",)


class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "code")


class AccountAdmin(admin.ModelAdmin):
    readonly_fields = (
        "acc_no",
        "debit",
        "credit",
        "available_balance",
        "pending_balance",
        "balance",
    )
    list_display = (
        "acc_no",
        "name",
        "date_created",
        "currency",
        "accounting_type",
        "internal_type",
        "state",
        "debit",
        "credit",
        "balance",
        "available_balance",
    )
    list_filter = ("accounting_type", "internal_type", "state")


class JournalAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "date_created", "journal_type")
    list_filter = ("journal_type",)


class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ("ref_no", "name", "date_created", "journal", "state")
    list_filter = ("journal",)


class JournalEntryLineAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "account",
        "description",
        "date_created",
        "state",
        "reconcile",
        "debit",
        "credit",
        "account_balance",
    )
    list_filter = ("state",)
    search_fields = ["account__name", "name"]


class ReconcileAdmin(admin.ModelAdmin):
    list_display = ("ref_no", "reconcile_type", "date_created")


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(CurrencyRate, CurrencyRateAdmin)
admin.site.register(AccountType, AccountTypeAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Journal, JournalAdmin)
admin.site.register(JournalEntry, JournalEntryAdmin)
admin.site.register(JournalEntryLine, JournalEntryLineAdmin)
admin.site.register(Reconcile, ReconcileAdmin)
