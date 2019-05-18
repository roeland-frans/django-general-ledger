from base.constants.bank import BANK_OTHER_CODE
from base.constants.entity import ENTITY_INDIVIDUAL
from base.constants.entity import ENTITY_PTY
from django.contrib.auth import get_user_model


def generate():
    objects = []

    # Users. (Manual create to set password)
    user, created = get_user_model().objects.get_or_create(username="admin")
    user.set_password("#C0mpl3t3!")
    user.is_active = True
    user.is_staff = True
    user.save()

    user, created = get_user_model().objects.get_or_create(
        username="system", first_name="System", last_name="System"
    )
    user.set_password("=<ewtc&e7*PM#C=E{$AWK+TXCL\X>Ykq+|7p*mR,FN^1fcP!~_")
    user.is_active = False
    user.save()

    user, created = get_user_model().objects.get_or_create(
        username="buyer@tradersvault.co.za",
        first_name="Buyer",
        last_name="Demo",
    )
    user.set_password("pass")
    user.email = "buyer@tradersvault.co.za"
    user.save()

    user, created = get_user_model().objects.get_or_create(
        username="seller@tradersvault.co.za",
        first_name="Seller",
        last_name="Demo",
    )
    user.set_password("pass")
    user.email = "seller@tradersvault.co.za"
    user.save()

    user, created = get_user_model().objects.get_or_create(
        username="affiliate@tradersvault.co.za",
        first_name="Affiliate",
        last_name="Demo",
    )
    user.set_password("pass")
    user.email = "affiliate@tradersvault.co.za"
    user.save()

    user, created = get_user_model().objects.get_or_create(
        username="partner@tradersvault.co.za",
        first_name="Partner",
        last_name="Demo",
    )
    user.set_password("pass")
    user.email = "partner@tradersvault.co.za"
    user.save()

    user, created = get_user_model().objects.get_or_create(
        username="vault@tradersvault.co.za",
        first_name="Vault",
        last_name="Demo",
    )
    user.set_password("pass")
    user.email = "admin@tradersvault.co.za"
    user.save()

    objects += [
        # Banks
        {
            "model": "base.Bank",
            "fields": {
                "code": "FNB",
                "name": "First National Bank",
                "validated_name": "FIRSTRAND BANK",
                "eft_branch_code": "250655",
                "can_verify_accounts": True,
            },
        },
        {
            "model": "base.Bank",
            "fields": {
                "code": "STD",
                "name": "Standard Bank",
                "eft_branch_code": "051001",
                "can_verify_accounts": True,
            },
        },
        {
            "model": "base.Bank",
            "fields": {
                "code": "ABSA",
                "name": "Absa Bank",
                "eft_branch_code": "632005",
                "can_verify_accounts": True,
            },
        },
        {
            "model": "base.Bank",
            "fields": {
                "code": "NED",
                "name": "Nedbank",
                "eft_branch_code": "198765",
                "can_verify_accounts": True,
            },
        },
        {
            "model": "base.Bank",
            "fields": {
                "code": "CAP",
                "name": "Capitec Bank",
                "eft_branch_code": "470010",
            },
        },
        {
            "model": "base.Bank",
            "fields": {
                "code": "BID",
                "name": "Bidvest Bank",
                "eft_branch_code": "462005",
            },
        },
        {
            "model": "base.Bank",
            "fields": {
                "code": "INV",
                "name": "Investec",
                "validated_name": "INVESTEC BANK LIMITED",
                "eft_branch_code": "580105",
            },
        },
        {
            "model": "base.Bank",
            "fields": {"code": str(BANK_OTHER_CODE), "name": "Other"},
        },
        # User profiles.
        {
            "model": "base.UserProfile",
            "fields": {
                "mobile": "27829348421",
                "id_no": "0000000000000",
                "user": {
                    "model": "base.User",
                    "fields": {"username": "admin"},
                },
            },
        },
        {
            "model": "base.UserProfile",
            "fields": {
                "mobile": "27829348421",
                "id_no": "0000000000001",
                "user": {
                    "model": "base.User",
                    "fields": {"username": "buyer@tradersvault.co.za"},
                },
            },
        },
        {
            "model": "base.UserProfile",
            "fields": {
                "mobile": "27829348421",
                "id_no": "0000000000002",
                "allow_api_access": True,
                "is_affiliate": True,
                "user": {
                    "model": "base.User",
                    "fields": {"username": "affiliate@tradersvault.co.za"},
                },
            },
        },
        {
            "model": "base.UserProfile",
            "fields": {
                "mobile": "27829348421",
                "id_no": "0000000000003",
                "allow_api_access": True,
                "is_partner": True,
                "user": {
                    "model": "base.User",
                    "fields": {"username": "partner@tradersvault.co.za"},
                },
            },
        },
        {
            "model": "base.UserProfile",
            "fields": {
                "mobile": "27829348421",
                "id_no": "0000000000004",
                "user": {
                    "model": "base.User",
                    "fields": {"username": "seller@tradersvault.co.za"},
                },
            },
        },
        {
            "model": "base.UserProfile",
            "fields": {
                "mobile": "27829348421",
                "id_no": "0000000000005",
                "user": {
                    "model": "base.User",
                    "fields": {"username": "vault@tradersvault.co.za"},
                },
            },
        },
        # TradersVault Entity and EntityBankAccount
        {
            "model": "base.Address",
            "fields": {
                "address": "123 Oak Avenue",
                "suburb": "Highveld",
                "city": "Centurion",
                "code": "0157",
                "country": "ZA",
                "province": "Gauteng",
            },
        },
        {
            "model": "base.Entity",
            "fields": {
                "entity_no": "000",
                "entity_type": ENTITY_PTY,
                "name": "TradersVault (Pty) Ltd",
                "reg_no": "00000",
                "telephone": "012 123 4567",
                "fax": "012 123 4567",
                "email": "info@tradersvault.co.za",
                "users": [
                    {
                        "model": "base.User",
                        "fields": {"username": "vault@tradersvault.co.za"},
                    }
                ],
                "physical_address": {
                    "model": "base.Address",
                    "fields": {"id": 1},
                },
                "postal_address": {
                    "model": "base.Address",
                    "fields": {"id": 1},
                },
            },
        },
        {
            "model": "base.EntityBankAccount",
            "fields": {
                "acc_no": "0000",
                "bank": {"model": "base.Bank", "fields": {"code": "FNB"}},
                "branch": "12345",
                "entity": {
                    "model": "base.Entity",
                    "fields": {"entity_no": "000"},
                },
            },
        },
        # Demo Buyer Entity and EntityBankAccount
        {
            "model": "base.Address",
            "fields": {
                "address": "456 Zip Avenue",
                "suburb": "Braamfontein",
                "city": "Johannesburg",
                "code": "0157",
                "country": "ZA",
                "province": "Gauteng",
            },
        },
        {
            "model": "base.Entity",
            "fields": {
                "entity_no": "111",
                "entity_type": ENTITY_INDIVIDUAL,
                "reg_no": "",
                "name": "Demo Buyer",
                "telephone": "012 123 4567",
                "fax": "012 123 4567",
                "email": "buyer@tradersvault.co.za",
                "users": [
                    {
                        "model": "base.User",
                        "fields": {"username": "buyer@tradersvault.co.za"},
                    }
                ],
                "physical_address": {
                    "model": "base.Address",
                    "fields": {"id": 2},
                },
                "postal_address": {
                    "model": "base.Address",
                    "fields": {"id": 2},
                },
            },
        },
        {
            "model": "base.EntityBankAccount",
            "fields": {
                "acc_no": "1111",
                "bank": {"model": "base.Bank", "fields": {"code": "STD"}},
                "branch": "12345",
                "entity": {
                    "model": "base.Entity",
                    "fields": {"entity_no": "111"},
                },
            },
        },
        # Demo Seller Entity and EntityBankAccount
        {
            "model": "base.Address",
            "fields": {
                "address": "456 Zero Avenue",
                "suburb": "Green Point",
                "city": "Cape Town",
                "code": "0157",
                "country": "ZA",
                "province": "Western Cape",
            },
        },
        {
            "model": "base.Entity",
            "fields": {
                "entity_no": "222",
                "entity_type": ENTITY_INDIVIDUAL,
                "name": "Demo Seller",
                "reg_no": "",
                "telephone": "012 123 4567",
                "fax": "012 123 4567",
                "email": "seller@tradersvault.co.za",
                "users": [
                    {
                        "model": "base.User",
                        "fields": {"username": "seller@tradersvault.co.za"},
                    }
                ],
                "physical_address": {
                    "model": "base.Address",
                    "fields": {"id": 3},
                },
                "postal_address": {
                    "model": "base.Address",
                    "fields": {"id": 3},
                },
            },
        },
        {
            "model": "base.EntityBankAccount",
            "fields": {
                "acc_no": "2222",
                "bank": {"model": "base.Bank", "fields": {"code": "BID"}},
                "branch": "12345",
                "entity": {
                    "model": "base.Entity",
                    "fields": {"entity_no": "222"},
                },
            },
        },
        # Demo Seller Business Entity and EntityBankAccount
        {
            "model": "base.Address",
            "fields": {
                "address": "567 Zero Avenue",
                "suburb": "Green Point",
                "city": "Cape Town",
                "code": "0157",
                "country": "ZA",
                "province": "Western Cape",
            },
        },
        {
            "model": "base.Entity",
            "fields": {
                "entity_no": "333",
                "entity_type": ENTITY_PTY,
                "reg_no": "33333",
                "name": "Seller Business",
                "telephone": "012 123 4567",
                "fax": "012 123 4567",
                "email": "seller@tradersvault.co.za",
                "users": [
                    {
                        "model": "base.User",
                        "fields": {"username": "seller@tradersvault.co.za"},
                    }
                ],
                "physical_address": {
                    "model": "base.Address",
                    "fields": {"id": 4},
                },
                "postal_address": {
                    "model": "base.Address",
                    "fields": {"id": 4},
                },
            },
        },
        {
            "model": "base.EntityBankAccount",
            "fields": {
                "acc_no": "3333",
                "bank": {"model": "base.Bank", "fields": {"code": "BID"}},
                "branch": "12345",
                "entity": {
                    "model": "base.Entity",
                    "fields": {"entity_no": "333"},
                },
            },
        },
        # Demo Partner Entity and EntityBankAccount
        {
            "model": "base.Address",
            "fields": {
                "address": "456 Zip Avenue",
                "suburb": "Braamfontein",
                "city": "Johannesburg",
                "code": "0157",
                "country": "ZA",
                "province": "Gauteng",
            },
        },
        {
            "model": "base.Entity",
            "fields": {
                "entity_no": "444",
                "entity_type": ENTITY_INDIVIDUAL,
                "reg_no": "",
                "name": "Demo Partner",
                "telephone": "012 123 4567",
                "fax": "012 123 4567",
                "email": "partner@tradersvault.co.za",
                "users": [
                    {
                        "model": "base.User",
                        "fields": {"username": "partner@tradersvault.co.za"},
                    }
                ],
                "physical_address": {
                    "model": "base.Address",
                    "fields": {"id": 2},
                },
                "postal_address": {
                    "model": "base.Address",
                    "fields": {"id": 2},
                },
            },
        },
        {
            "model": "base.EntityBankAccount",
            "fields": {
                "acc_no": "4444",
                "bank": {"model": "base.Bank", "fields": {"code": "STD"}},
                "branch": "12345",
                "entity": {
                    "model": "base.Entity",
                    "fields": {"entity_no": "444"},
                },
            },
        },
    ]

    return objects
