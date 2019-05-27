from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from moneyed.classes import CURRENCIES

# The accounting types of an Account model
ACCOUNT_ASSET = "ASSET"
ACCOUNT_LIABILITY = "LIABILITY"
ACCOUNT_INCOME = "INCOME"
ACCOUNT_EXPENSE = "EXPENSE"
ACCOUNT_CAPITAL = "CAPITAL"

ACCOUNT_TYPES_ADMIN = (
    (ACCOUNT_ASSET, _("Asset")),
    (ACCOUNT_LIABILITY, _("Liability")),
    (ACCOUNT_INCOME, _("Income")),
    (ACCOUNT_EXPENSE, _("Expense")),
    (ACCOUNT_CAPITAL, _("Capital")),
)

STATE_OPEN = "OPEN"
STATE_CLOSED = "CLOSED"
STATE_SUSPENDED = "SUSPENDED"
STATE_LIMITED = "LIMITED"

ACCOUNT_STATES_ADMIN = (
    (STATE_OPEN, _("Open")),
    (STATE_CLOSED, _("Closed")),
    (STATE_SUSPENDED, _("Suspended")),
    (STATE_LIMITED, _("Limited")),
)

# The default internal account types of an Account model
GENERAL_ACCOUNT = "GENERAL"
BANK_ACCOUNT = "BANK"

ACCOUNT_INTERNAL_TYPES = {
    GENERAL_ACCOUNT: "General Account",
    BANK_ACCOUNT: "Bank Account",
}

ROOT_ACC_NO = "00000000000"

# The default journal types of a Journal model
JOURNAL_GENERAL = "GENERAL"
JOURNAL_SALE = "SALE"
JOURNAL_PURCHASE = "PURCHASE"
JOURNAL_CASH = "CASH"
JOURNAL_BANK = "BANK"

JOURNAL_TYPES_ADMIN = (
    (JOURNAL_GENERAL, _("General")),
    (JOURNAL_SALE, _("Sale")),
    (JOURNAL_PURCHASE, _("Purchase")),
    (JOURNAL_CASH, _("Cash")),
    (JOURNAL_BANK, _("Bank")),
)

# The states of a JournalEntry model
JOURNAL_ENTRY_POSTED = "POSTED"
JOURNAL_ENTRY_UNPOSTED = "UNPOSTED"
JOURNAL_ENTRY_RECONCILED = "RECONCILED"

JOURNAL_ENTRY_STATES_ADMIN = (
    (JOURNAL_ENTRY_POSTED, _("Posted")),
    (JOURNAL_ENTRY_UNPOSTED, _("Unposted")),
    (JOURNAL_ENTRY_RECONCILED, _("Reconciled")),
)

# The type of a JournalEntryLine model
DEBIT = "D"
CREDIT = "C"

JOURNAL_ENTRY_LINE_TYPES = ((DEBIT, _("Debit")), (CREDIT, _("Credit")))

# The states of a JournalEntryLine
JOURNAL_ENTRY_LINE_POSTED = "POSTED"
JOURNAL_ENTRY_LINE_UNPOSTED = "UNPOSTED"
JOURNAL_ENTRY_LINE_RECONCILE = "RECONCILE"
JOURNAL_ENTRY_LINE_LOADED = "LOADED"
JOURNAL_ENTRY_LINE_FAILED = "FAILED"

JOURNAL_ENTRY_LINE_STATES_ADMIN = (
    (JOURNAL_ENTRY_LINE_POSTED, _("Posted")),
    (JOURNAL_ENTRY_LINE_UNPOSTED, _("Unposted")),
    (JOURNAL_ENTRY_LINE_RECONCILE, _("Reconciled")),
)

# Reconcile types
RECONCILE_GENERAL = "GENERAL"
RECONCILE_BANK = "BANK"

RECONCILE_TYPES = (RECONCILE_GENERAL, RECONCILE_BANK)

RECONCILE_TYPES_ADMIN = (
    (RECONCILE_GENERAL, _("General")),
    (RECONCILE_BANK, _("Bank")),
)

if getattr(settings, "BASE_CURRENCY"):
    BASE_CURRENCY = CURRENCIES[settings.BASE_CURRENCY]
else:
    # Default currency is USD
    BASE_CURRENCY = CURRENCIES["USD"]
