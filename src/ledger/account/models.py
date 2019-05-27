from account.constants.account import ACCOUNT_ASSET
from account.constants.account import ACCOUNT_CAPITAL
from account.constants.account import ACCOUNT_EXPENSE
from account.constants.account import ACCOUNT_INCOME
from account.constants.account import ACCOUNT_LIABILITY
from account.constants.account import ACCOUNT_STATES_ADMIN
from account.constants.account import ACCOUNT_TYPES_ADMIN
from account.constants.account import BASE_CURRENCY
from account.constants.account import CREDIT
from account.constants.account import DEBIT
from account.constants.account import JOURNAL_ENTRY_LINE_POSTED
from account.constants.account import JOURNAL_ENTRY_LINE_RECONCILE
from account.constants.account import JOURNAL_ENTRY_LINE_STATES_ADMIN
from account.constants.account import JOURNAL_ENTRY_LINE_UNPOSTED
from account.constants.account import JOURNAL_ENTRY_POSTED
from account.constants.account import JOURNAL_ENTRY_STATES_ADMIN
from account.constants.account import JOURNAL_ENTRY_UNPOSTED
from account.constants.account import JOURNAL_TYPES_ADMIN
from account.constants.account import RECONCILE_BANK
from account.constants.account import RECONCILE_GENERAL
from account.constants.account import RECONCILE_TYPES
from account.constants.account import RECONCILE_TYPES_ADMIN
from account.constants.account import STATE_OPEN
from datetime import datetime
from decimal import ROUND_HALF_EVEN
from decimal import Decimal
from django import dispatch
from django.db import models
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from djmoney.models.fields import MoneyField
from moneyed.classes import Money
from uuid import uuid4

# Custom signals
account_credit_signal = dispatch.Signal(
    providing_args=["account", "amount", "type", "name", "desc"]
)
account_debit_signal = dispatch.Signal(
    providing_args=["account", "amount", "type", "name", "desc"]
)


def round_amount(amount):
    exp = Decimal(10) ** -2

    if isinstance(amount, Money):
        amount.amount = amount.amount.quantize(
            exp=exp, rounding=ROUND_HALF_EVEN
        )
        return amount

    if not isinstance(amount, Decimal):
        amount = Decimal(amount)

    return amount.quantize(exp=exp, rounding=ROUND_HALF_EVEN)


class AccountError(Exception):
    """
    A general Account error.
    """

    pass


class JournalEntryError(Exception):
    """
    A general JournalEntry error occurred.
    """

    pass


class JournalEntryLineError(Exception):
    """
    A general JournalEntryLine error occurred.
    """

    pass


class Currency(models.Model):
    """
    This is the system wide Currency model.
    """

    code = models.CharField(
        _("Currency Code"),
        max_length=10,
        unique=True,
        help_text=_("International currency code i.e. ZAR"),
    )
    name = models.CharField(
        _("Currency Name"),
        max_length=100,
        help_text=_("Common name of the currency i.e. Rand"),
    )
    is_base = models.BooleanField(
        _("Base"),
        default=False,
        help_text=_(
            "If selected this currency's rate will be treated as "
            "base rate against which all other conversions will be "
            "made."
        ),
    )
    current_rate = models.DecimalField(
        _("Current Rate"),
        max_digits=13,
        decimal_places=8,
        help_text="Current conversion rate as in relation to base currency.",
    )
    date = models.DateTimeField(_("Date"))

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

    def __str__(self):
        return "%s (%s) %s" % (self.code, self.name, self.current_rate)

    def convert_to(self, amount, to_currency):
        """
        Converts the given amount into the given currency.
        @param amount: The decimal amount to use.
        @param to_currency: The currency to convert to.
        @return Returns a Money() instance in the destination currency and converted amount.
        """
        if self.code == to_currency:
            return Money(amount, to_currency)

        currency = Currency.objects.get(code=to_currency)
        from_rate = self.current_rate
        to_rate = currency.current_rate

        return Decimal(to_rate / from_rate) * Money(amount, to_currency)

    def convert_from(self, amount, from_currency):
        """
        Converts the given amount from the given currency.
        @param amount: The decimal amount to use.
        @param to_currency: The currency to convert to.
        @return Returns a Money() instance in the destination currency and converted amount.
        """
        if self.code == from_currency:
            return Money(amount, from_currency)

        currency = Currency.objects.get(code=from_currency)
        from_rate = currency.current_rate
        to_rate = self.current_rate

        return Decimal(to_rate / from_rate) * Money(amount, self.code)


class CurrencyRate(models.Model):
    """
    This is the Currency Rate that will be for a given date.
    """

    rate = models.DecimalField(
        _("Rate"),
        decimal_places=8,
        max_digits=13,
        help_text=_(
            "Current conversion rate as in relation to base currency."
        ),
    )
    date_from = models.DateTimeField(
        _("Date From"), help_text="Date from which conversion rate applies."
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="rates",
        blank=False,
        null=False,
        help_text=_("Currency to which rate relates."),
    )

    class Meta:
        verbose_name = _("Currency Rate")
        verbose_name_plural = _("Currency Rates")

    def __str__(self):
        return str(self.date_from)


class AccountType(models.Model):
    """
    This is the database model for the an account type. This type is for
    internal use and is not be confused with the accounting type.

    For example a Vault account, or Bank account, used internaly to group
    accounts for filtering etc.
    """

    code = models.CharField(
        _("Code"), max_length=50, unique=True, help_text=_("The type Code")
    )
    name = models.CharField(
        _("Name"), max_length=100, help_text=_("The name of the type")
    )

    class Meta:
        verbose_name = _("Account Type")
        verbose_name_plural = _("Account Types")

    def __str__(self):
        return self.name


class Account(models.Model):
    """
    This is the database model for the an account. An account is a financial
    container that an entity uses for financial transactions and services. It
    is generic in that it has a balance and associated transactions.
    """

    acc_no = models.CharField(
        _("Account Number"),
        max_length=50,
        unique=True,
        help_text=_("The Account Number"),
    )
    name = models.CharField(max_length=128, blank=True, null=True)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    last_activity = models.DateTimeField(_("Last Activity"), auto_now_add=True)
    accounting_type = models.CharField(
        _("Account Type"),
        max_length=50,
        choices=ACCOUNT_TYPES_ADMIN,
        help_text=_(
            "Account type applicable to accounting rules i.e. "
            "asset, liability."
        ),
    )
    debit = MoneyField(
        _("Debit"),
        max_digits=20,
        decimal_places=2,
        default_currency=BASE_CURRENCY.code,
        default=Decimal(0),
    )
    credit = MoneyField(
        _("Credit"),
        max_digits=20,
        decimal_places=2,
        default_currency=BASE_CURRENCY.code,
        default=Decimal(0),
    )
    balance = MoneyField(
        _("Balance"),
        max_digits=40,
        decimal_places=2,
        default_currency=BASE_CURRENCY.code,
        default=Decimal(0),
    )
    available_balance = MoneyField(
        _("Available Balance"),
        max_digits=40,
        decimal_places=2,
        default_currency=BASE_CURRENCY.code,
        default=Decimal(0),
    )
    pending_balance = MoneyField(
        _("Pending Balance"),
        max_digits=40,
        decimal_places=2,
        default_currency=BASE_CURRENCY.code,
        default=Decimal(0),
    )
    state = models.CharField(
        _("State"),
        max_length=20,
        choices=ACCOUNT_STATES_ADMIN,
        default=STATE_OPEN,
    )
    internal_type = models.ForeignKey(
        AccountType,
        on_delete=models.CASCADE,
        related_name="type_accounts",
        null=False,
        blank=False,
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="accounts",
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

    def __str__(self):
        return "%s - %s (%s)" % (self.acc_no, self.name, self.balance)

    def save(self, *args, **kwargs):
        """
        Set/check unique generated account number.
        """
        # Generate a unique account number if one does not exist.
        if not self.acc_no:
            self.acc_no = f"A{uuid4().hex}"
        self.last_activity = datetime.now()
        return super(Account, self).save(*args, **kwargs)

    def select_for_update(self):
        """
        This must be used with in a transaction block and will lock the account row until
        the transaction is committed. This will ensure that the in-memory balances are in
        sync with db for the duration of the transaction blocking other pending transactions
        on this row.
        """
        tmp_account = Account.objects.select_for_update().get(
            acc_no=self.acc_no
        )
        self.debit = tmp_account.debit
        self.credit = tmp_account.credit
        self.balance = tmp_account.balance
        self.available_balance = tmp_account.available_balance
        self.pending_balance = tmp_account.pending_balance

    def zero_balances(self, save_acc=True):
        """
        Convenience function to zero all the balances correctly.
        """
        self.balance = Money(Decimal(0), self.currency.code)
        self.available_balance = Money(Decimal(0), self.currency.code)
        self.pending_balance = Money(Decimal(0), self.currency.code)
        self.debit = Money(Decimal(0), self.currency.code)
        self.credit = Money(Decimal(0), self.currency.code)
        if save_acc:
            self.save()

    @transaction.atomic()
    def update_balance(self, debit, credit, save_acc=True):
        """
        This will update the current account balance with the given debit/credit
        values. The account balance will increase/decrease depending on it's
        accounting type. NB. The given debit/credit values must be rounded.
        """
        # Convert the given debit/credit to account currency.
        if isinstance(debit, Money):
            debit = self.currency.convert_from(
                amount=debit.amount, from_currency=debit.currency.code
            )
        else:
            debit = Money(debit, self.currency.code)

        if isinstance(credit, Money):
            credit = self.currency.convert_from(
                amount=credit.amount, from_currency=credit.currency.code
            )
        else:
            credit = Money(credit, self.currency.code)

        # Make sure the amounts are rounded
        debit = round_amount(debit)
        credit = round_amount(credit)

        tmp_balance = Money(0, self.currency.code)

        # Do a select_for_update to lock the row and make sure all money fields are sync'd
        self.select_for_update()

        self.debit += debit
        self.credit += credit

        if (
            self.accounting_type == ACCOUNT_ASSET
            or self.accounting_type == ACCOUNT_EXPENSE
        ):
            tmp_balance += debit
            tmp_balance -= credit
            balance_check = self.debit - self.credit
        elif (
            self.accounting_type == ACCOUNT_LIABILITY
            or self.accounting_type == ACCOUNT_INCOME
            or self.accounting_type == ACCOUNT_CAPITAL
        ):
            tmp_balance -= debit
            tmp_balance += credit
            balance_check = self.credit - self.debit
        else:
            raise AccountError(
                "Could not update account balance, the account has no valid accounting type."
            )

        self.balance += tmp_balance
        self.available_balance += tmp_balance

        if self.balance != balance_check:
            raise AccountError(
                "Updated balance does not match the difference between Debit/Credit on Account."
            )

        self.last_activity = datetime.now()

        # Write the balance to the db
        self.save()
        return self.balance

    @transaction.atomic()
    def new_available_balance(self, delta):
        """
        This will update the available balance given from the current balance
        with the delta added.
        @param delta: The amount to adjust the balance by.
        """
        # Convert the given amount to the account's currency.
        if isinstance(delta, Money):
            delta = self.currency.convert_from(
                amount=delta.amount, from_currency=delta.currency.code
            )
        else:
            delta = Money(delta, self.currency.code)

        # Make sure input amounts are rounded
        delta = round_amount(delta)

        # Do a select_for_update to lock the row and make sure all money fields are sync'd
        self.select_for_update()

        self.last_activity = datetime.now()
        self.available_balance = self.balance + delta

        # Write the new balance to the db
        self.save()
        return self.available_balance

    @transaction.atomic()
    def _update_balance_field(self, amount, balance_field, operator):
        """
        This is a convenience method that will execute a raw SQL query to update the given balance
        by the given amount. The actual calculation gets done by the db in a transaction which ensures the balance
        is always updated using the latest balance value in the db.
        @param amount: The amount to update the balance by.
        @param balance_field: The name of the balance field, this must be one of the balance field defined
                              on the model.
        @param operator: Either a '+' or '-'.
        @returns Returns the new balance as returned by the query.
        """
        # Check parameters before proceeding
        if not hasattr(self, balance_field):
            raise AccountError(
                "Uknown balance field %s specified" % balance_field
            )
        if operator not in ["-", "+"]:
            raise AccountError(
                "Operator %s is not supported by update_balance_field"
                % operator
            )

        # Convert the given amount to the account's currency.
        if isinstance(amount, Money):
            amount = self.currency.convert_from(
                amount=amount.amount, from_currency=amount.currency.code
            )
        else:
            amount = Money(amount, self.currency.code)

        # Make sure input amounts are rounded
        amount = round_amount(amount)

        if amount.amount < Decimal(0):
            raise AccountError(
                "Given amount must be positive to update %s." % balance_field
            )

        # Do a select_for_update to lock the row and make sure all money fields are sync'd
        self.select_for_update()

        self.last_activity = datetime.now()

        if balance_field == "available_balance":
            if operator == "+":
                self.available_balance += amount
            else:
                self.available_balance -= amount
            return_balance = self.available_balance

        elif balance_field == "pending_balance":
            if operator == "+":
                self.pending_balance += amount
            else:
                self.pending_balance -= amount
            return_balance = self.pending_balance
        else:
            raise AccountError(
                "Given balance field %s is not supported by update_balance_field"
                % balance_field
            )

        # Write the new balance to the db
        self.save()
        return return_balance

    def increase_available_balance(self, amount):
        """
        This will increase the current available balance by the given amount.
        @param amount: The amount to increase the available balance by.
        """
        new_balance = self._update_balance_field(
            amount, "available_balance", "+"
        )
        return new_balance

    def decrease_available_balance(self, amount):
        """
        This will decreate the current available balance by the given amount.
        @param amount: The amount to decrease the available balance by.
        """
        new_balance = self._update_balance_field(
            amount, "available_balance", "-"
        )
        return new_balance

    def increase_pending_balance(self, amount):
        """
        This will increase the current pending balance by the given amount.
        @param amount: The amount to increase the pending balance by.
        """
        new_balance = self._update_balance_field(
            amount, "pending_balance", "+"
        )
        return new_balance

    def decrease_pending_balance(self, amount):
        """
        This will increase the current pending balance by the given amount.
        @param amount: The amount to increase the pending balance by.
        """
        new_balance = self._update_balance_field(
            amount, "pending_balance", "-"
        )
        return new_balance


class Journal(models.Model):
    """
    This is the database model for an accounting Journal.

    Glues account moves together, used internally for accounting/auditing
    purposes.
    """

    code = models.CharField(
        _("Code"), max_length=50, unique=True, help_text=_("The Journal code")
    )
    name = models.CharField(
        _("Name"), max_length=100, help_text=_("The Journal name")
    )
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    journal_type = models.CharField(
        _("Journal Type"),
        max_length=50,
        choices=JOURNAL_TYPES_ADMIN,
        help_text=_(
            "Account type applicable to accounting rules i.e. sale, purchase."
        ),
    )
    debit_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="debit_journals",
        blank=True,
        null=True,
        help_text=_("Default debit account for journal"),
    )
    credit_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="credit_journals",
        blank=True,
        null=True,
        help_text=_("Default credit account for journal"),
    )
    control_accounts = models.ManyToManyField(
        Account, related_name="control_journals", blank=True
    )

    class Meta:
        verbose_name = _("Journal")
        verbose_name_plural = _("Journals")

    def __str__(self):
        return self.name


class JournalEntry(models.Model):
    """
    A Journal entry, consisting of a collection of entry lines, with the debit
    and credit ammounts of each line having to be balanced for an entry to be
    valid.
    """

    ref_no = models.CharField(
        _("Reference"),
        max_length=50,
        unique=True,
        help_text=_("The Journal code"),
    )
    name = models.CharField(
        _("Name"), max_length=400, help_text=_("The Journal name")
    )
    date_created = models.DateTimeField(_("Date Created"))
    journal = models.ForeignKey(
        Journal,
        on_delete=models.CASCADE,
        related_name="account_moves",
        blank=False,
        null=False,
    )
    state = models.CharField(
        _("State"),
        max_length=64,
        choices=JOURNAL_ENTRY_STATES_ADMIN,
        default=JOURNAL_ENTRY_UNPOSTED,
    )

    class Meta:
        verbose_name = _("Journal Entry")
        verbose_name_plural = _("Journal Entries")

    def __str__(self):
        return self.ref_no

    def save(self, *args, **kwargs):
        """
        Set/check unique generated reference number.
        @todo: implement
        """
        if not self.ref_no:
            self.ref_no = f"J{uuid4().hex}"
        if not self.date_created:
            self.date_created = datetime.now()
        return super(JournalEntry, self).save(*args, **kwargs)

    def get_debit_lines(self):
        """
        This will return a QuerySet of all the Debit journal entries.
        """
        return self.entry_lines.filter(line_type=DEBIT)

    def get_credit_lines(self):
        """
        This will return a QuerySet of all the credit journal entries.
        """
        return self.entry_lines.filter(line_type=CREDIT)

    @transaction.atomic
    def post(self):
        """
        This will attempt to post the Journal Entry, it first checks if the
        debit/credit totals of the journal entry lines balance and then it will
        proceed to update the balance of each account associated with each
        journal entry line.
        """
        tot_debit = Decimal(0)
        tot_credit = Decimal(0)
        entry_lines = self.entry_lines.filter(
            state=JOURNAL_ENTRY_LINE_UNPOSTED
        )

        if entry_lines.count() <= 0:
            raise JournalEntryError(
                "Cannot post a Journal Entry with no lines."
            )

        base_currency = Currency.objects.get(code=BASE_CURRENCY.code)

        for line in entry_lines:
            tot_debit += base_currency.convert_from(
                amount=line.debit.amount,
                from_currency=line.debit.currency.code,
            ).amount
            tot_credit += base_currency.convert_from(
                amount=line.credit.amount,
                from_currency=line.credit.currency.code,
            ).amount

        if tot_debit != tot_credit:
            raise JournalEntryError(
                "Debit/Credit must balance for a Journal Entry"
            )

        for line in entry_lines:
            line.post()

        self.state = JOURNAL_ENTRY_POSTED
        self.save()

    @transaction.atomic
    def create_transfer(
        self, from_acc, to_acc, amount, name=None, desc=None, return_dict=False
    ):
        """
        Creates a simple funds transfer from one account to another.
        """
        if not isinstance(amount, Money):
            # Assume the amount is in the same currency as from account currency
            amount = Money(amount, from_acc.currency.code)

        # Make sure input amount is rounded
        amount = round_amount(amount)

        # Determine the debit/credit account
        from_type = from_acc.accounting_type
        to_type = to_acc.accounting_type

        assets = [ACCOUNT_ASSET, ACCOUNT_EXPENSE]
        liabilities = [ACCOUNT_LIABILITY, ACCOUNT_INCOME, ACCOUNT_CAPITAL]

        if from_type in assets and to_type in assets:
            debit_acc = to_acc
            credit_acc = from_acc

        elif from_type in liabilities and to_type in liabilities:
            debit_acc = from_acc
            credit_acc = to_acc

        else:
            debit_acc = from_acc
            credit_acc = to_acc

        return self.create_balanced_entry(
            debit_acc=debit_acc,
            credit_acc=credit_acc,
            amount=amount,
            name=name,
            desc=desc,
            return_dict=return_dict,
        )

    def create_balanced_entry(
        self,
        debit_acc,
        credit_acc,
        amount,
        name=None,
        desc=None,
        return_dict=False,
    ):
        """
        This creates a balanced entry meaning two entry lines with the same
        amount debit and credit. This is a convenience function to give a
        shortcut for creating simple balanced entries. It posts the journal
        entry lines and updates the account balances.

        @return: If return_dict is True it will return a dictionary containing
        the debit and credit lines that were generated.
        """
        if not isinstance(debit_acc, Account):
            raise TypeError(
                "Cannot create balance entry, '%s' is not a valid Account"
                % debit_acc
            )
        if not isinstance(credit_acc, Account):
            raise TypeError(
                "Cannot create balance entry, '%s' is not a valid Account"
                % credit_acc
            )
        if not isinstance(amount, Money):
            raise TypeError("Given amount must be of type Money")
        if debit_acc == credit_acc:
            raise JournalEntryError(
                "Cannot create a balanced entry on the same Account"
            )

        # Get the correct debit/credit amounts in their respective currencies
        debit = debit_acc.currency.convert_from(
            amount=amount.amount, from_currency=amount.currency.code
        )
        credit = credit_acc.currency.convert_from(
            amount=amount.amount, from_currency=amount.currency.code
        )

        debit_desc = None
        credit_desc = None
        if isinstance(desc, list):
            if len(desc) >= 2:
                debit_desc = desc[0]
                credit_desc = desc[1]
        elif desc:
            debit_desc = desc
            credit_desc = desc

        if not debit_desc:
            debit_desc = "'%s' debited." % debit_acc.acc_no
        if not credit_desc:
            credit_desc = "'%s' credited." % credit_acc.acc_no

        # Create atomic context make sure all db related changes are rolled back upon exception.
        # Exceptions will be propagated as usual.
        with transaction.atomic():
            debit_line = JournalEntryLine()
            debit_line.journal_entry = self
            debit_line.account = debit_acc
            debit_line.ref_no = self.ref_no
            debit_line.date_created = self.date_created
            debit_line.description = debit_desc
            if name:
                debit_line.name = name
            else:
                debit_line.name = "#DEBIT"
            debit_line.set_debit(debit)

            credit_line = JournalEntryLine()
            credit_line.journal_entry = self
            credit_line.account = credit_acc
            credit_line.ref_no = self.ref_no
            credit_line.date_created = self.date_created
            credit_line.description = credit_desc
            if name:
                credit_line.name = name
            else:
                credit_line.name = "#CREDIT"
            credit_line.set_credit(credit)

            self.entry_lines.add(debit_line, credit_line)

            # Post all the entries
            debit_line.post()
            credit_line.post()

            self.state = JOURNAL_ENTRY_POSTED
            self.save()

        # Only send signals after successful commit of accounting posts
        account_debit_signal.send(
            sender=self.__class__,
            account=debit_acc,
            amount=debit,
            type=DEBIT,
            name=debit_line.name,
            desc=debit_desc,
        )
        account_credit_signal.send(
            sender=self.__class__,
            account=credit_acc,
            amount=credit,
            type=CREDIT,
            name=credit_line.name,
            desc=credit_desc,
        )

        if return_dict:
            return {DEBIT: debit_line, CREDIT: credit_line}

    def add_debit_line(self, debit_acc, amount, date_created, name, desc=None):
        if type(debit_acc) != Account:
            raise TypeError(
                "Cannot create balance entry, '%s' is not a valid Account"
                % debit_acc
            )

        if isinstance(amount, Money):
            # Do the currency conversion
            debit = debit_acc.currency.convert_from(
                amount=amount.amount, from_currency=amount.currency.code
            )
        else:
            # Assume the amount is in the same currency as given account
            debit = Money(amount, debit_acc.currency.code)

        debit_line = JournalEntryLine()
        debit_line.journal_entry = self
        debit_line.account = debit_acc
        debit_line.date_created = date_created
        debit_line.ref_no = self.ref_no
        debit_line.name = name
        debit_line.set_debit(debit)

        if desc:
            debit_line.description = desc
        else:
            debit_line.description = "'%s' debited." % debit_acc.acc_no

        self.entry_lines.add(debit_line)

        return debit_line

    def add_credit_line(
        self, credit_acc, amount, date_created, name, desc=None
    ):
        if type(credit_acc) != Account:
            raise TypeError(
                "Cannot create balance entry, '%s' is not a valid Account"
                % credit_acc
            )

        if isinstance(amount, Money):
            # Do the currency conversion
            credit = credit_acc.currency.convert_from(
                amount=amount.amount, from_currency=amount.currency.code
            )
        else:
            # Assume the amount is in the same currency as given account
            credit = Money(amount, credit_acc.currency.code)

        # Make sure the debit amount is rounded
        credit = round_amount(credit)

        credit_line = JournalEntryLine()
        credit_line.journal_entry = self
        credit_line.account = credit_acc
        credit_line.date_created = date_created
        credit_line.ref_no = self.ref_no
        credit_line.name = name
        credit_line.set_credit(credit)

        if desc:
            credit_line.description = desc
        else:
            credit_line.description = "'%s' credited." % credit_acc.acc_no

        self.entry_lines.add(credit_line)

        return credit_line

    def reconcile_entry(self, reconcile_type=RECONCILE_GENERAL):
        """
        This is a convenience method to create a reconciliation for the entry's
        entry lines.
        @param reconcile_type: The type of reconciliation.
        """
        if not reconcile_type in RECONCILE_TYPES:
            raise AccountError(
                "Cannot reconcile journal entry, incorrect reconcile type: %s"
                % reconcile_type
            )

        recon = Reconcile()
        recon.reconcile_type = reconcile_type
        recon.save()

        entry_lines = self.entry_lines.all()

        for line in entry_lines:
            line.reconcile_line(recon)

        return recon

    def bank_reconcile_entry(self):
        """
        This will do a bank reconciliation on the entry.
        """
        return self.reconcile_entry(RECONCILE_BANK)


class JournalEntryLine(models.Model):
    """
    Contains accounting detail for an account transaction, used in conjunction
    with JournalEntries to populate Journals.
    """

    ref_no = models.CharField(_("Reference"), max_length=50)
    name = models.CharField(
        _("Name"),
        max_length=200,
        help_text=_("Descriptive Name"),
        blank=True,
        null=True,
    )
    date_created = models.DateTimeField(_("Date Created"))
    line_type = models.CharField(
        _("Line Type"),
        max_length=10,
        blank=False,
        null=False,
        default="N",  # This is a bogus default value, see self.save()
    )
    debit = MoneyField(
        _("Debit"),
        max_digits=20,
        decimal_places=2,
        default_currency=BASE_CURRENCY.code,
        default=Decimal(0),
    )
    credit = MoneyField(
        _("Credit"),
        max_digits=20,
        decimal_places=2,
        default_currency=BASE_CURRENCY.code,
        default=Decimal(0),
    )
    account_balance = MoneyField(
        _("Account Balance"),
        max_digits=40,
        decimal_places=2,
        default_currency=BASE_CURRENCY.code,
        default=Decimal(0),
    )
    description = models.CharField(_("Description"), max_length=400)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="account_entry_lines",
        blank=False,
        null=False,
    )
    journal_entry = models.ForeignKey(
        JournalEntry,
        on_delete=models.CASCADE,
        related_name="entry_lines",
        blank=False,
        null=False,
    )
    reconcile = models.ForeignKey(
        "Reconcile",
        on_delete=models.CASCADE,
        related_name="reconcile_lines",
        blank=True,
        null=True,
    )
    state = models.CharField(
        _("State"),
        max_length=64,
        choices=JOURNAL_ENTRY_LINE_STATES_ADMIN,
        default=JOURNAL_ENTRY_LINE_UNPOSTED,
    )

    class Meta:
        verbose_name = _("Journal Entry Line")
        verbose_name_plural = _("Journal Entry Lines")

    def __str__(self):
        return self.ref_no

    def set_debit(self, value):
        """
        This will set the debit value and clear the credit value.
        @param value: The given debit value.
        """
        self.debit = round_amount(value)
        self.credit = Money(0, value.currency)
        self.line_type = DEBIT

    def set_credit(self, value):
        """
        This will set the credit value and clear the debit value.
        @param value: The given credit value.
        """
        self.debit = Money(0, value.currency)
        self.credit = round_amount(value)
        self.line_type = CREDIT

    def post(self):
        """
        This will attempt to post the JournalEntryLine changing it's state from
        UNPOSTED to POSTED.
        """
        if self.state == JOURNAL_ENTRY_LINE_POSTED:
            raise JournalEntryLineError("JournalEntryLine is already posted.")

        balance = self.account.update_balance(
            debit=self.debit, credit=self.credit
        )
        self.account_balance = balance
        self.state = JOURNAL_ENTRY_LINE_POSTED

        self.save()

    def reconcile_line(self, reconcile):
        """
        This will reconcile the JournalEntryLine and change the state to
        'RECON'.
        @param reconcile: The Reconcile object.
        """
        if not isinstance(reconcile, Reconcile):
            raise TypeError("Invalid Reconcile object %s" % reconcile)

        self.reconcile = reconcile
        self.state = JOURNAL_ENTRY_LINE_RECONCILE
        self.save()

    @property
    def statement_amount(self):
        if self.line_type == DEBIT:
            return -1 * self.debit
        else:
            return self.credit

    def save(self, *args, **kwargs):
        """
        Set/check unique generated reference number.
        @todo: implement
        """
        if not self.date_created:
            self.date_created = datetime.now()

        if self.line_type == "N":
            if self.debit.amount > Decimal(
                0
            ) and self.credit.amount == Decimal(0):
                self.line_type = DEBIT
            elif self.debit.amount == Decimal(
                0
            ) and self.credit.amount > Decimal(0):
                self.line_type = CREDIT
            else:
                raise JournalEntryLineError(
                    "JournalEntryLine must either have a Debit value OR a Credit value greater than 0.0"
                )

        elif self.debit.amount > Decimal(0) and self.credit.amount > Decimal(
            0
        ):
            raise JournalEntryLineError(
                "JournalEntryLine cannot have a Debit AND Credit value that are both greater than 0.0"
            )

        return super(JournalEntryLine, self).save(*args, **kwargs)


class Reconcile(models.Model):
    """
    This keeps track of JournalEntryLine reconciliations.
    """

    ref_no = models.CharField(_("Reference"), max_length=50)
    reconcile_type = models.CharField(
        _("Reconcile Type"),
        max_length=10,
        choices=RECONCILE_TYPES_ADMIN,
        blank=False,
        null=False,
        default=RECONCILE_GENERAL,
    )
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("Reconcile")
        verbose_name_plural = _("Reconciliations")

    def __str__(self):
        return self.ref_no

    def save(self, *args, **kwargs):
        """
        Set/check unique generated ref number.
        """
        # Generate a unique reference number if one does not exist.
        if not self.ref_no:
            self.ref_no = f"R{uuid4().hex}"
        return super(Reconcile, self).save(*args, **kwargs)
