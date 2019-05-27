from account.constants import account
from datetime import datetime


def generate():
    objects = []

    objects += [
        # Currencies
        {
            "model": "account.Currency",
            "fields": {
                "code": str(account.BASE_CURRENCY.code),
                "name": str(account.BASE_CURRENCY.name),
                "is_base": True,
                "current_rate": 1.0,
                "date": str(datetime.now()),
            },
        },
        # Currency Rates
        {
            "model": "account.CurrencyRate",
            "fields": {
                "rate": 1.0,
                "date_from": str(datetime.now()),
                "currency": {
                    "model": "account.Currency",
                    "fields": {"code": str(account.BASE_CURRENCY.code)},
                },
            },
        },
        # Account Types
        {
            "model": "account.AccountType",
            "fields": {
                "code": account.GENERAL_ACCOUNT,
                "name": account.ACCOUNT_INTERNAL_TYPES[
                    account.GENERAL_ACCOUNT
                ],
            },
        },
        {
            "model": "account.AccountType",
            "fields": {
                "code": account.BANK_ACCOUNT,
                "name": account.ACCOUNT_INTERNAL_TYPES[account.BANK_ACCOUNT],
            },
        },
        # Create root TradersVault Vault account
        {
            "model": "account.Account",
            "fields": {
                "acc_no": account.ROOT_ACC_NO,
                "name": "Root TradersVault Account",
                "date_created": str(datetime.now()),
                "accounting_type": account.ACCOUNT_LIABILITY,
                "debit": 0.0,
                "debit_currency": str(account.BASE_CURRENCY.code),
                "credit": 0.0,
                "credit_currency": str(account.BASE_CURRENCY.code),
                "balance": 0.0,
                "balance_currency": str(account.BASE_CURRENCY.code),
                "available_balance": 0.0,
                "available_balance_currency": str(account.BASE_CURRENCY.code),
                "internal_type": {
                    "model": "account.AccountType",
                    "fields": {"code": account.GENERAL_ACCOUNT},
                },
                "entity": {
                    "model": "base.Entity",
                    "fields": {"entity_no": "000"},
                },
                "currency": {
                    "model": "account.Currency",
                    "fields": {"code": str(account.BASE_CURRENCY.code)},
                },
            },
        },
    ]

    return objects
