from account.constants.account import BASE_CURRENCY
from decimal import Decimal
from django.db import models
from django.utils.translation import ugettext_lazy as _
from djmoney.models.fields import MoneyField
from ledger_api.constants import BANK_IMPORT_LINE_NEW
from ledger_api.constants import BANK_IMPORT_LINE_STATE_ADMIN


class BankStatementImportLine(models.Model):
    uuid = models.CharField(
        _("UUID"),
        max_length=100,
        unique=True,
        help_text=_(
            "Unique id which will be used when posting the transaction into the accounting system"
        ),
    )
    hash = models.CharField(
        _("HASH"),
        max_length=100,
        unique=True,
        help_text=_(
            "Unique hash generated from the line sequence no, date, amount, reference"
        ),
    )
    weak_hash = models.CharField(
        _("Weak HASH"),
        max_length=100,
        unique=True,
        help_text=_(
            "Unique hash generated from the line date, amount, reference"
        ),
    )
    ref_no = models.CharField(_("Reference"), max_length=50)
    state = models.CharField(
        _("State"),
        max_length=64,
        choices=BANK_IMPORT_LINE_STATE_ADMIN,
        default=BANK_IMPORT_LINE_NEW,
    )
    date_created = models.DateTimeField(_("Date Created"))
    line_type = models.CharField(
        _("Line Type"),
        max_length=10,
        blank=False,
        null=False,
        default="N",  # This is a bogus default value, see self.save()
    )
    amount = MoneyField(
        _("Amount"),
        max_digits=20,
        decimal_places=2,
        default=Decimal(0),
        default_currency=BASE_CURRENCY.code,
    )

    class Meta:
        verbose_name = _("Bank Statement Import Line")
        verbose_name_plural = _("Bank Statement Import Lines")

    def __unicode__(self):
        return "Import Line(%s)" % self.ref_no
