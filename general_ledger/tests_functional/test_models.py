from constants.account import ACCOUNT_LIABILITY
from constants.account import BASE_CURRENCY
from constants.account import JOURNAL_GENERAL
from datetime import datetime
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.test import TransactionTestCase
from models import Account
from models import AccountType
from models import Currency
from models import Journal
from models import JournalEntry
from moneyed.classes import Money


def setUpModule():
    call_command("flush", interactive=False, verbosity=0)


class BaseAccountTestCase(object):
    @classmethod
    def setUpClass(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", password="test"
        )

        # Create require data objects
        cls.account_type = AccountType.objects.create(code="TEST", name="Test")
        cls.zar = Currency.objects.create(
            code=BASE_CURRENCY.code,
            name="Rand",
            is_base=True,
            current_rate=Decimal(1.0),
            date=datetime.now(),
        )

        # Create a General Journal
        cls.gen_jnl = Journal.objects.create(
            code="GEN-JNL",
            name="General Journal",
            journal_type=JOURNAL_GENERAL,
        )

    @classmethod
    def tearDownClass(cls):
        cls.gen_jnl.delete()
        cls.zar.delete()
        cls.account_type.delete()
        cls.user.delete()


class BalanceRoundingError(BaseAccountTestCase, TestCase):
    """
    24 May 2014
    This error was observed when a specified amount with a certain decimal
    accuracy was posted to the accounting system that the debit & credit balances
    were 1c out and any further accounting posts would fail.
    """

    @classmethod
    def setUpClass(cls):
        super(BalanceRoundingError, cls).setUpClass()

        # Create the Buyer and Seller accounts
        cls.buyer = Account.objects.create(
            acc_no="111",
            name="Buyer Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_LIABILITY,
            internal_type=cls.account_type,
            currency=cls.zar,
        )

        cls.seller = Account.objects.create(
            acc_no="222",
            name="Selelr Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_LIABILITY,
            internal_type=cls.account_type,
            currency=cls.zar,
        )

    @classmethod
    def tearDownClass(cls):
        cls.buyer.delete()
        cls.seller.delete()
        super(BalanceRoundingError, cls).tearDownClass()

    def setUp(self):
        self.buyer.zero_balances(False)
        self.buyer.balance = Decimal(500)
        self.buyer.credit = Decimal(500)
        self.buyer.save()

        self.seller.zero_balances()

    def test_balance_error_on_threshold(self):
        # Test with given amount
        amount = Money(119.8255, BASE_CURRENCY.code)

        deposit = JournalEntry.objects.create(
            name="Error Transaction 1", journal=self.gen_jnl
        )
        deposit.create_transfer(
            from_acc=self.buyer,
            to_acc=self.seller,
            amount=amount,
            name="Test Error Transaction 1",
            desc="Test Error Transaction 1",
        )

        # Test that the buyer balances are correct, ROUND_HALF_EVEN rounds 119.8255 to 119.83
        self.assertEqual(self.buyer.balance, Money(380.17, BASE_CURRENCY.code))
        self.assertEqual(self.buyer.debit, Money(119.83, BASE_CURRENCY.code))
        self.assertEqual(self.buyer.credit, Money(500, BASE_CURRENCY.code))

        # Test that the seller balances are correct
        self.assertEqual(
            self.seller.balance, Money(119.83, BASE_CURRENCY.code)
        )
        self.assertEqual(self.seller.debit, Money(0, BASE_CURRENCY.code))
        self.assertEqual(self.seller.credit, Money(119.83, BASE_CURRENCY.code))

    def test_balance_error_below_threshold(self):
        # Test with given amount
        amount = Money(119.8245, BASE_CURRENCY.code)

        deposit = JournalEntry.objects.create(
            name="Error Transaction 2", journal=self.gen_jnl
        )
        deposit.create_transfer(
            from_acc=self.buyer,
            to_acc=self.seller,
            amount=amount,
            name="Test Error Transaction 2",
            desc="Test Error Transaction 2",
        )

        # Test that the buyer balances are correct, ROUND_HALF_EVEN rounds 119.8245 to 119.82
        self.assertEqual(self.buyer.balance, Money(380.18, BASE_CURRENCY.code))
        self.assertEqual(self.buyer.debit, Money(119.82, BASE_CURRENCY.code))
        self.assertEqual(self.buyer.credit, Money(500, BASE_CURRENCY.code))

        # Test that the seller balances are correct
        self.assertEqual(
            self.seller.balance, Money(119.82, BASE_CURRENCY.code)
        )
        self.assertEqual(self.seller.debit, Money(0, BASE_CURRENCY.code))
        self.assertEqual(self.seller.credit, Money(119.82, BASE_CURRENCY.code))

    def test_balance_error_above_threshold(self):
        # Test with given amount
        amount = Money(119.8265, BASE_CURRENCY.code)

        deposit = JournalEntry.objects.create(
            name="Error Transaction 3", journal=self.gen_jnl
        )
        deposit.create_transfer(
            from_acc=self.buyer,
            to_acc=self.seller,
            amount=amount,
            name="Test Error Transaction 3",
            desc="Test Error Transaction 3",
        )

        # Test that the buyer balances are correct, ROUND_HALF_EVEN rounds 119.8265 to 119.83
        self.assertEqual(self.buyer.balance, Money(380.17, BASE_CURRENCY.code))
        self.assertEqual(self.buyer.debit, Money(119.83, BASE_CURRENCY.code))
        self.assertEqual(self.buyer.credit, Money(500, BASE_CURRENCY.code))

        # Test that the seller balances are correct
        self.assertEqual(
            self.seller.balance, Money(119.83, BASE_CURRENCY.code)
        )
        self.assertEqual(self.seller.debit, Money(0, BASE_CURRENCY.code))
        self.assertEqual(self.seller.credit, Money(119.83, BASE_CURRENCY.code))


class AccountBalanceUpdates(TransactionTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="test"
        )

        # Create require data objects
        self.account_type = AccountType.objects.create(
            code="TEST", name="Test"
        )
        self.zar = Currency.objects.create(
            code=BASE_CURRENCY.code,
            name="Rand",
            is_base=True,
            current_rate=Decimal(1.0),
            date=datetime.now(),
        )

        # Create a General Journal
        self.gen_jnl = Journal.objects.create(
            code="GEN-JNL",
            name="General Journal",
            journal_type=JOURNAL_GENERAL,
        )

        # Create the Buyer and Seller accounts
        self.account = Account.objects.create(
            acc_no="111",
            name="Test Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_LIABILITY,
            internal_type=self.account_type,
            currency=self.zar,
        )

    def test_single_update(self):
        self.account.zero_balances()

        amount = Decimal(100)
        self.account.update_balance(Decimal(0), amount)

        self.assertEqual(self.account.balance.amount, Decimal(100))
        self.assertEqual(self.account.available_balance.amount, Decimal(100))
        self.assertEqual(self.account.debit.amount, Decimal(0))
        self.assertEqual(self.account.credit.amount, Decimal(100))

    def test_update_stale_object(self):
        account = Account.objects.get(
            acc_no=self.account.acc_no
        )  # Balance is 0
        account_stale = Account.objects.get(
            acc_no=self.account.acc_no
        )  # Balance is 0

        # Account balance should be 50.0
        account.update_balance(debit=Decimal(0), credit=Decimal(50))
        self.assertEqual(account.balance.amount, Decimal(50))
        self.assertEqual(account.available_balance.amount, Decimal(50))
        self.assertEqual(account.debit.amount, Decimal(0))
        self.assertEqual(account.credit.amount, Decimal(50))

        # Account balance should be 100.0
        account_stale.update_balance(debit=Decimal(0), credit=Decimal(50))
        self.assertEqual(account_stale.balance.amount, Decimal(100))
        self.assertEqual(account_stale.available_balance.amount, Decimal(100))
        self.assertEqual(account_stale.debit.amount, Decimal(0))
        self.assertEqual(account_stale.credit.amount, Decimal(100))
