from django.utils.translation import ugettext_lazy as _

DEFAULT_ENTITY_NO = "000"

ENTITY_INDIVIDUAL = "INDIVIDUAL"
ENTITY_SOLE_PROPRIETOR = "SOLE_PROPRIETOR"
ENTITY_PARTNERSHIP = "PARTNERSHIP"
ENTITY_CC = "CC"
ENTITY_PTY = "PTY"
ENTITY_LTD = "LTD"
ENTITY_NGO = "NGO"
ENTITY_NPO = "NPO"

ENTITY_TYPES = (
    (ENTITY_INDIVIDUAL, _("Personal")),
    (ENTITY_SOLE_PROPRIETOR, _("Sole Proprietor")),
    (ENTITY_PARTNERSHIP, _("Partnership")),
    (ENTITY_CC, _("Closed Corporation")),
    (ENTITY_PTY, _("Private Company")),
    (ENTITY_LTD, _("Public Company")),
    (ENTITY_NGO, _("National Government Organisation")),
    (ENTITY_NPO, _("Non-Profit Organisation")),
)

ENTITY_TYPES_NON_INDIVIDUAL = [
    entity_type
    for entity_type in ENTITY_TYPES
    if entity_type[0] != ENTITY_INDIVIDUAL
]
