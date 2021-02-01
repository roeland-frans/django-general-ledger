from django.utils.translation import ugettext_lazy as _

# The states of a JournalEntryLine
BANK_IMPORT_LINE_NEW = "NEW"
BANK_IMPORT_LINE_DUPLICATE = "DUPLICATE"

BANK_IMPORT_LINE_STATE_ADMIN = (
    (BANK_IMPORT_LINE_NEW, _("New")),
    (BANK_IMPORT_LINE_DUPLICATE, _("Duplicate")),
)
