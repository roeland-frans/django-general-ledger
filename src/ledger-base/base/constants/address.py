from django.utils.translation import ugettext_lazy as _

ADDRESS_PHYSICAL = "PHYSICAL"
ADDRESS_POSTAL = "POSTAL"

ADDRESS_TYPES = (
    (ADDRESS_PHYSICAL, _("Physical Address")),
    (ADDRESS_POSTAL, _("Postal Address")),
)
