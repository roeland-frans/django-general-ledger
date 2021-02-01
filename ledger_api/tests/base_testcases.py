from account.constants.account import ACCOUNT_ASSET
from account.constants.account import ACCOUNT_INCOME
from account.constants.account import ACCOUNT_LIABILITY
from account.constants.account import BANK_ACCOUNT
from account.constants.account import BASE_CURRENCY
from account.constants.account import GENERAL_ACCOUNT
from account.constants.account import JOURNAL_GENERAL
from account.constants.account import ROOT_ACC_NO
from account.models import Account
from account.models import AccountType
from account.models import Currency
from account.models import Journal
from base.constants.entity import ENTITY_INDIVIDUAL
from base.constants.entity import ENTITY_PTY
from base.models import Bank
from base.models import Entity
from base.models import EntityBankAccount
from base.models import UserProfile
from datetime import datetime
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase


class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # Create require data objects.
        cls.account_type, created = AccountType.objects.get_or_create(
            code="TEST", defaults={"name": "Test"}
        )
        cls.general_account_type, created = AccountType.objects.get_or_create(
            code=GENERAL_ACCOUNT, defaults={"name": "General Account"}
        )
        cls.bank_account_type, created = AccountType.objects.get_or_create(
            code=BANK_ACCOUNT, defaults={"name": "Bank Account"}
        )
        cls.currency, created = Currency.objects.get_or_create(
            code=BASE_CURRENCY.code,
            defaults={
                "name": "Rand",
                "is_base": True,
                "current_rate": Decimal(1.0),
                "date": datetime.now(),
            },
        )
        # Create buyer and seller entities and accounts and users.
        cls.root_entity, created = Entity.objects.get_or_create(
            entity_no="000",
            defaults={
                "name": "TradersVault",
                "entity_type": ENTITY_PTY,
                "telephone": "0111234567",
                "email": "test@tradersvault.co.za",
            },
        )
        cls.buyer_entity, created = Entity.objects.get_or_create(
            entity_no="111",
            defaults={
                "name": "Test Buyer Entity",
                "entity_type": ENTITY_INDIVIDUAL,
                "telephone": "0111234567",
                "email": "testbuyer@tradersvault.co.za",
            },
        )
        cls.seller_entity, created = Entity.objects.get_or_create(
            entity_no="222",
            defaults={
                "name": "Test Seller Entity",
                "entity_type": ENTITY_INDIVIDUAL,
                "telephone": "0111234567",
                "email": "testseller@tradersvault.co.za",
            },
        )
        cls.buyer_account, created = Account.objects.get_or_create(
            acc_no="111",
            defaults={
                "name": "Test Buyer Account",
                "date_created": datetime.now(),
                "accounting_type": ACCOUNT_LIABILITY,
                "debit": 0.0,
                "credit": 0.0,
                "balance": 0.0,
                "internal_type": "TRADERS",
                "currency": cls.currency,
                "entity": cls.buyer_entity,
            },
        )
        cls.seller_account, created = Account.objects.get_or_create(
            acc_no="222",
            defaults={
                "name": "Test Seller Account",
                "date_created": datetime.now(),
                "accounting_type": ACCOUNT_LIABILITY,
                "debit": 0.0,
                "credit": 0.0,
                "balance": 0.0,
                "internal_type": "TRADERS",
                "currency": cls.currency,
                "entity": cls.seller_entity,
            },
        )
        cls.root_account, created = Account.objects.get_or_create(
            acc_no=ROOT_ACC_NO,
            defaults={
                "name": "TradersVault",
                "date_created": datetime.now(),
                "accounting_type": ACCOUNT_LIABILITY,
                "debit": 0.0,
                "credit": 0.0,
                "balance": 0.0,
                "internal_type": "TRADERS",
                "currency": cls.currency,
                "entity": cls.seller_entity,
            },
        )
        cls.buyer, created = get_user_model().objects.get_or_create(
            username="buyer",
            defaults={"email": "buyer@tradersvault.co.za", "password": "pass"},
        )
        cls.buyer_entity.users.add(cls.buyer)
        cls.buyer_profile, created = UserProfile.objects.get_or_create(
            email_secondary="buyer@gmail.com",
            defaults={
                "mobile": "0821234567",
                "user": cls.buyer,
                "id_no": "8406075147083",
            },
        )
        cls.seller, created = get_user_model().objects.get_or_create(
            username="seller",
            defaults={
                "email": "seller@tradersvault.co.za",
                "password": "pass",
            },
        )
        cls.seller_entity.users.add(cls.seller)
        cls.seller_profile, created = UserProfile.objects.get_or_create(
            email_secondary="seller@gmail.com",
            defaults={
                "mobile": "0821234567",
                "user": cls.seller,
                "passport_no": "123456789",
                "passport_country": "ZA_GP",
                "dob": datetime.now(),
            },
        )
        cls.deal_income_account = Account.objects.create(
            acc_no="444556",
            name="Test Income Deal Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_INCOME,
            debit=0.0,
            credit=0.0,
            balance=0.0,
            internal_type=cls.account_type,
            currency=cls.currency,
        )
        # Create the test Account
        cls.account = Account.objects.create(
            acc_no="11111111111",
            name="Buyer Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_LIABILITY,
            internal_type=cls.account_type,
            currency=cls.currency,
        )
        # Create the test Account
        cls.bank_account = Account.objects.create(
            acc_no="123456",
            name="Bank Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_ASSET,
            internal_type=cls.account_type,
            currency=cls.currency,
        )
        cls.fnb = Bank.objects.create(name="FNB", code="11111")
        cls.gen_jnl = Journal.objects.create(
            code="GEN-JNL",
            name="General Journal",
            journal_type=JOURNAL_GENERAL,
        )
        cls.entity = Entity.objects.create(
            entity_type=ENTITY_INDIVIDUAL,
            name="Buyer Demo",
            telephone="0123456789",
            email="buyer@tradersvault.co.za",
        )
        cls.entity_bank_account = EntityBankAccount.objects.create(
            acc_no="123456", entity=cls.entity, bank=cls.fnb, branch="123456"
        )
        cls.entity.current_bank_account = cls.entity_bank_account

    @classmethod
    def tearDownClass(cls):
        cls.seller_profile.delete()
        cls.seller.delete()
        cls.buyer_profile.delete()
        cls.buyer.delete()
        cls.root_account.delete()
        cls.seller_account.delete()
        cls.buyer_account.delete()
        cls.seller_entity.delete()
        cls.buyer_entity.delete()
        cls.root_entity.delete()
        cls.billing_jnl.delete()
        cls.deal_jnl.delete()
        cls.currency.delete()
        cls.general_account_type.delete()
        cls.bank_account_type.delete()
        cls.account_type.delete()
        cls.deal_income_account.delete()
        cls.deal_billing_item.delete()
        cls.entity_bank_account.delete()
        cls.entity.delete()
        cls.gen_jnl.delete()
        cls.fnb.delete()
        cls.bank_account.delete()
        cls.account.delete()
