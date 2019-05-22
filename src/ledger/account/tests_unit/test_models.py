from account.constants.account import ACCOUNT_ASSET
from account.constants.account import ACCOUNT_CAPITAL
from account.constants.account import ACCOUNT_EXPENSE
from account.constants.account import ACCOUNT_INCOME
from account.constants.account import ACCOUNT_LIABILITY
from account.constants.account import BASE_CURRENCY
from account.constants.account import CREDIT
from account.constants.account import DEBIT
from account.constants.account import JOURNAL_ENTRY_LINE_POSTED
from account.constants.account import JOURNAL_ENTRY_LINE_RECONCILE
from account.constants.account import JOURNAL_ENTRY_LINE_UNPOSTED
from account.constants.account import JOURNAL_ENTRY_POSTED
from account.constants.account import JOURNAL_GENERAL
from account.constants.account import RECONCILE_BANK
from account.constants.account import RECONCILE_GENERAL
from account.models import Account
from account.models import AccountError
from account.models import AccountType
from account.models import Currency
from account.models import CurrencyRate
from account.models import Journal
from account.models import JournalEntry
from account.models import JournalEntryError
from account.models import JournalEntryLine
from account.models import JournalEntryLineError
from account.models import Reconcile
from account.models import round_amount
from datetime import datetime
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from moneyed.classes import Money
from unittest.mock import MagicMock
from unittest.mock import patch


class RoundAmountTestCase(TestCase):
    def test_round_amount(self):
        amount = Money("100.1255", BASE_CURRENCY)
        amount = round_amount(amount)

        self.assertEqual(amount, Money("100.13", BASE_CURRENCY))

        amount = "100.1255"
        amount = round_amount(amount)
        self.assertEqual(amount, Decimal("100.13"))


class CurrencyTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.zar = Currency.objects.create(
            code=BASE_CURRENCY.code,
            name="Rand",
            is_base=True,
            current_rate=Decimal(1.0),
            date=datetime.now(),
        )

        cls.usd = Currency.objects.create(
            code="USD",
            name="Dollar",
            is_base=True,
            current_rate=Decimal(0.1),
            date=datetime.now(),
        )

    @classmethod
    def tearDownClass(cls):
        cls.zar.delete()
        cls.usd.delete()

    def test_unicode(self):
        text = self.zar.__unicode__()
        self.assertEqual(
            text,
            "%s (%s) %s"
            % (self.zar.code, self.zar.name, self.zar.current_rate),
        )

    def test_convert_to(self):
        # Test that a Money object gets returned with the same currency
        amount = self.zar.convert_to(1000.0, BASE_CURRENCY.code)
        self.assertEqual(amount, Money(1000.0, BASE_CURRENCY.code))

        # Test that the correct conversion is done
        amount = self.zar.convert_to(1000.0, "USD")
        self.assertEqual(amount, Money(100.0, "USD"))

    def test_convert_from(self):
        # Test that a Money object gets returned with the same currency
        amount = self.zar.convert_from(1000.0, BASE_CURRENCY.code)
        self.assertEqual(amount, Money(1000.0, BASE_CURRENCY.code))

        # Test that the correct conversion is done
        amount = self.zar.convert_from(1000.0, "USD")
        self.assertEqual(amount, Money(10000.0, BASE_CURRENCY.code))


class CurrencyRateTestCase(TestCase):
    def test_unicode(self):
        rate = CurrencyRate()
        now = datetime.now()
        rate.date_from = now

        text = rate.__unicode__()
        self.assertEqual(text, str(now))


class AccountTypeTestCase(TestCase):
    def test_unicode(self):
        account_type = AccountType()
        account_type.code = "NEW TYPE"
        account_type.name = "New Type"

        text = account_type.__unicode__()
        self.assertEqual(text, account_type.name)


class AccountTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", password="test"
        )
        # Create require data objects
        cls.account_type = AccountType.objects.create(code="TEST", name="Test")
        cls.currency = Currency.objects.create(
            code=BASE_CURRENCY.code,
            name="Rand",
            is_base=True,
            current_rate=Decimal(1.0),
            date=datetime.now(),
        )
        cls.usd = Currency.objects.create(
            code="USD",
            name="Dollar",
            is_base=True,
            current_rate=Decimal(0.1),
            date=datetime.now(),
        )

        # Create the Buyer and Seller accounts
        cls.account = Account.objects.create(
            acc_no="111",
            name="Buyer Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_LIABILITY,
            internal_type=cls.account_type,
            currency=cls.currency,
        )

    @classmethod
    def tearDownClass(cls):
        cls.account.delete()
        cls.currency.delete()
        cls.usd.delete()
        cls.account_type.delete()
        cls.user.delete()

    def test_unicode(self):
        text = self.account.__unicode__()

        self.assertEqual(
            text,
            "%s - %s (%s)"
            % (self.account.acc_no, self.account.name, self.account.balance),
        )

    @patch("account.models.datetime")
    @patch("account.models.random")
    @patch("django.db.models.base.Model.save")
    @patch("account.models.connection")
    def test_save(self, connection, save, random, datetime):
        # Configure mocks
        cursor_mock = MagicMock(name="cursor")

        connection.cursor.return_value = cursor_mock

        random.randint.return_value = 1000

        date_mock = MagicMock(name="date")
        date_mock.strftime.return_value = "20140101"
        datetime.now.return_value = date_mock

        account = Account()
        account.name = "Buyer Account"
        account.date_created = datetime.now()
        account.accounting_type = ACCOUNT_LIABILITY
        account.debit = 0.0
        account.credit = 0.0
        account.balance = 0.0
        account.internal_type = self.account_type
        account.currency = self.currency

        account.save()

        assert datetime.now.called
        date_mock.strftime.assert_called_with("%Y%m%d")
        self.assertEqual(account.acc_no, "13593175616")

        save.called = None

        account.acc_no = None
        account.save()

        assert save.called
        self.assertEqual(account.acc_no, "13593175616")

    def test_zero_balances(self):
        account = Account()
        account.save = MagicMock(name="save")
        account.balance = 100.23
        account.available_balance = 200.23
        account.debit = 400.23
        account.credit = 500.23
        account.currency = self.currency

        # Test with save_acc=True
        account.zero_balances()

        self.assertEqual(account.balance.amount, Decimal(0.0))
        self.assertEqual(account.available_balance.amount, Decimal(0.0))
        self.assertEqual(account.debit.amount, Decimal(0.0))
        self.assertEqual(account.credit.amount, Decimal(0.0))
        assert account.save.called

        # Test with save_acc=False
        account.save = MagicMock(name="save")
        account.balance = Money(100.23, BASE_CURRENCY)
        account.available_balance = Money(200.23, BASE_CURRENCY)
        account.debit = Money(400.23, BASE_CURRENCY)
        account.credit = Money(500.23, BASE_CURRENCY)

        account.zero_balances(save_acc=False)

        self.assertEqual(account.balance.amount, Decimal(0.0))
        self.assertEqual(account.available_balance.amount, Decimal(0.0))
        self.assertEqual(account.debit.amount, Decimal(0.0))
        self.assertEqual(account.credit.amount, Decimal(0.0))
        assert not account.save.called

    def test_update_balance(self):
        # Test that the currency convert method gets called
        debit = Money(0.0, BASE_CURRENCY.code)
        credit = Money(100.0, BASE_CURRENCY.code)
        self.account.zero_balances()

        with patch(
            "account.models.Currency.convert_from",
            return_value=Money(1000.0, BASE_CURRENCY.code),
        ) as convert_from:
            new_balance = self.account.update_balance(
                debit=debit, credit=credit, save_acc=False
            )
            convert_from.assert_called_with(
                amount=credit.amount, from_currency=credit.currency.code
            )
            self.assertEqual(len(convert_from.mock_calls), 2)
            self.assertEqual(new_balance.amount, 0.0)

        # Test that the currency gets converted
        self.account.zero_balances()
        debit = Money(0, "USD")
        credit = Money(112.23, "USD")

        new_balance = self.account.update_balance(debit=debit, credit=credit)
        self.assertEqual(self.account.balance, Money(1122.30, BASE_CURRENCY))
        self.assertEqual(new_balance, Money(1122.30, BASE_CURRENCY))

        # Balance should increase if Account is Asset and debit amount given
        self.account.accounting_type = ACCOUNT_ASSET
        self.account.zero_balances()

        new_balance = self.account.update_balance(1000.0, 0.0)

        self.assertEqual(self.account.balance, Money(1000.0, BASE_CURRENCY))
        self.assertEqual(new_balance, Money(1000.0, BASE_CURRENCY))

        # Balance should decrease if Account is Asset and credit amount given
        self.account.accounting_type = ACCOUNT_ASSET
        self.account.zero_balances()

        new_balance = self.account.update_balance(0.0, 1000.0)

        self.assertEqual(self.account.balance, Money(-1000.0, BASE_CURRENCY))
        self.assertEqual(new_balance, Money(-1000.0, BASE_CURRENCY))

        # Balance should decrease if Account is Liability and debit amount given
        self.account.accounting_type = ACCOUNT_LIABILITY
        self.account.zero_balances()

        new_balance = self.account.update_balance(1000.0, 0.0)

        self.assertEqual(self.account.balance, Money(-1000.0, BASE_CURRENCY))
        self.assertEqual(new_balance, Money(-1000.0, BASE_CURRENCY))

        # Balance should increase if Account is Liability and credit amount given
        self.account.accounting_type = ACCOUNT_LIABILITY
        self.account.zero_balances()

        new_balance = self.account.update_balance(0.0, 1000.0)

        self.assertEqual(self.account.balance, Money(1000.0, BASE_CURRENCY))
        self.assertEqual(new_balance, Money(1000.0, BASE_CURRENCY))

        # Balance should decrease if Account is Income and debit amount given
        self.account.accounting_type = ACCOUNT_INCOME
        self.account.zero_balances()

        new_balance = self.account.update_balance(1000.0, 0.0)

        self.assertEqual(self.account.balance, Money(-1000.0, BASE_CURRENCY))
        self.assertEqual(new_balance, Money(-1000.0, BASE_CURRENCY))

        # Balance should increase if Account is Income and credit amount given
        self.account.accounting_type = ACCOUNT_INCOME
        self.account.zero_balances()

        new_balance = self.account.update_balance(0.0, 1000.0)

        self.assertEqual(self.account.balance, Money(1000.0, BASE_CURRENCY))
        self.assertEqual(new_balance, Money(1000.0, BASE_CURRENCY))

        # Balance should increase if Account is Expense and debit amount given
        self.account.accounting_type = ACCOUNT_EXPENSE
        self.account.zero_balances()

        new_balance = self.account.update_balance(1000, 0.0)

        self.assertEqual(self.account.balance, Money(1000.0, BASE_CURRENCY))
        self.assertEqual(new_balance, Money(1000.0, BASE_CURRENCY))

        # Balance should decrease if Account is Expense and credit amount given
        self.account.accounting_type = ACCOUNT_EXPENSE
        self.account.zero_balances()

        new_balance = self.account.update_balance(0.0, 1000.0)

        self.assertEqual(self.account.balance, Money(-1000.0, BASE_CURRENCY))
        self.assertEqual(new_balance, Money(-1000.0, BASE_CURRENCY))

        # Balance should decrease if Account is Captial and debit amount given
        self.account.accounting_type = ACCOUNT_CAPITAL
        self.account.zero_balances()

        new_balance = self.account.update_balance(1000.0, 0.0)

        self.assertEqual(self.account.balance, Money(-1000.0, BASE_CURRENCY))
        self.assertEqual(new_balance, Money(-1000.0, BASE_CURRENCY))

        # Balance should increase if Account is Capital and credit amount given
        self.account.accounting_type = ACCOUNT_CAPITAL
        self.account.zero_balances()

        new_balance = self.account.update_balance(0.0, 1000.0)

        self.assertEqual(self.account.balance, Money(1000.0, BASE_CURRENCY))
        self.assertEqual(new_balance, Money(1000.0, BASE_CURRENCY))

        # Test with out saving to the db
        self.account.accounting_type = ACCOUNT_CAPITAL
        self.account.zero_balances()

        new_balance = self.account.update_balance(0.0, 1000.0, save_acc=False)

        self.assertEqual(self.account.balance, Money(1000.0, BASE_CURRENCY))
        self.assertEqual(new_balance, Money(1000.0, BASE_CURRENCY))

        # With bogus debit credit values and balance there should be a mismatch
        # between the updated balance and the difference between Debit/Credit,
        # this should raise AccountError
        self.account.zero_balances()
        self.account.accounting_type = ACCOUNT_CAPITAL
        self.account.debit = Decimal(1000.0)
        self.account.credit = Decimal(500.0)
        self.account.balance = Decimal(0.0)
        self.account.save()
        self.assertRaises(
            AccountError, self.account.update_balance, 0.0, 1000.0
        )

        # If Accounting Type is a bogus value then it should raise AccountError
        self.account.accounting_type = "RANDOM"
        self.assertRaises(
            AccountError, self.account.update_balance, debit=0.0, credit=0.0
        )

    def test_new_available_balance(self):
        account = Account.objects.create(
            acc_no="667365522288993",
            name="New Available Balance Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_LIABILITY,
            internal_type=self.account_type,
            currency=self.currency,
        )

        # Test that the currency convert method gets called
        with patch(
            "account.models.Currency.convert_from",
            return_value=Money(1000.0, BASE_CURRENCY.code),
        ) as convert_from:
            amount = Money(100.0, BASE_CURRENCY.code)
            new_balance = account.new_available_balance(amount)
            convert_from.assert_called_with(
                amount=amount.amount, from_currency=amount.currency.code
            )
            self.assertEqual(new_balance, Money(1000.0, BASE_CURRENCY.code))

        # Test that the database gets updated correctly
        new_balance = account.new_available_balance(1000.0)

        account = Account.objects.get(pk=account.pk)
        self.assertEqual(new_balance, Money(1000.0, BASE_CURRENCY.code))
        self.assertEqual(
            account.available_balance, Money(1000.0, BASE_CURRENCY.code)
        )

        # Clean up
        account.delete()

    def test_update_balance_field(self):
        account = Account.objects.create(
            acc_no="667365522288993",
            name="New Available Balance Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_LIABILITY,
            internal_type=self.account_type,
            currency=self.currency,
        )

        # Test if it raises AccountError with negative amount
        self.assertRaises(
            AccountError,
            account._update_balance_field,
            amount=-1000.00,
            balance_field="available_balance",
            operator="-",
        )

        # Test if it raises AccountError with a bogus balance_field
        self.assertRaises(
            AccountError,
            account._update_balance_field,
            amount=1000.00,
            balance_field="bogus_balance",
            operator="-",
        )

        # Test if it raises AccountError with a bogus operator
        self.assertRaises(
            AccountError,
            account._update_balance_field,
            amount=1000.00,
            balance_field="available_balance",
            operator="*",
        )

        # Test that the currency convert method gets called
        with patch(
            "account.models.Currency.convert_from",
            return_value=Money(1000.0, BASE_CURRENCY.code),
        ) as convert_from:
            amount = Money(100.0, BASE_CURRENCY.code)
            new_balance = account._update_balance_field(
                amount=amount, balance_field="available_balance", operator="+"
            )
            convert_from.assert_called_with(
                amount=amount.amount, from_currency=amount.currency.code
            )
            self.assertEqual(new_balance, Money(1000.0, BASE_CURRENCY.code))
            self.assertEqual(
                account.available_balance, Money(1000.0, BASE_CURRENCY.code)
            )

        # Test that the available balance gets increased
        account.zero_balances()

        new_balance = account._update_balance_field(
            amount=1000.0, balance_field="available_balance", operator="+"
        )

        account = Account.objects.get(pk=account.pk)
        self.assertEqual(new_balance, Money(1000.0, BASE_CURRENCY.code))
        self.assertEqual(
            account.available_balance, Money(1000.0, BASE_CURRENCY.code)
        )

        # Test that the available balance gets decreased
        account.zero_balances()

        new_balance = account._update_balance_field(
            amount=1000.0, balance_field="available_balance", operator="-"
        )

        account = Account.objects.get(pk=account.pk)
        self.assertEqual(new_balance, Money(-1000.0, BASE_CURRENCY.code))
        self.assertEqual(
            account.available_balance, Money(-1000.0, BASE_CURRENCY.code)
        )

        # Test that the pending balance gets increased
        account.pending_balance = Money(Decimal(0), self.currency.code)
        account.zero_balances()

        new_balance = account._update_balance_field(
            amount=1000.0, balance_field="pending_balance", operator="+"
        )

        account = Account.objects.get(pk=account.pk)
        self.assertEqual(new_balance, Money(1000.0, BASE_CURRENCY.code))
        self.assertEqual(
            account.pending_balance, Money(1000.0, BASE_CURRENCY.code)
        )

        # Test that the pending balance gets decreased
        account.pending_balance = Money(Decimal(0), self.currency.code)
        account.zero_balances()

        new_balance = account._update_balance_field(
            amount=1000.0, balance_field="pending_balance", operator="-"
        )

        account = Account.objects.get(pk=account.pk)
        self.assertEqual(new_balance, Money(-1000.0, BASE_CURRENCY.code))
        self.assertEqual(
            account.pending_balance, Money(-1000.0, BASE_CURRENCY.code)
        )

        # Clean up
        account.delete()

    def test_increase_available_balance(self):
        account = Account.objects.create(
            name="Buyer Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_LIABILITY,
            internal_type=self.account_type,
            currency=self.currency,
        )

        expected_balance = Money(1000.0, self.currency.code)

        # Test if the available balance increase by 1000 ZAR
        new_balance = account.increase_available_balance(1000.0)

        account = Account.objects.get(pk=account.pk)
        self.assertEqual(new_balance, expected_balance)
        self.assertEqual(account.available_balance, expected_balance)

        # Clean up
        account.delete()

    def test_decrease_available_balance(self):
        account = Account.objects.create(
            name="Buyer Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_LIABILITY,
            internal_type=self.account_type,
            currency=self.currency,
            available_balance=Decimal(1000),
        )

        expected_balance = Money(0.0, self.currency.code)

        # Test if the available balance increase by 1000 ZAR
        new_balance = account.decrease_available_balance(1000.0)

        account = Account.objects.get(pk=account.pk)
        self.assertEqual(new_balance, expected_balance)
        self.assertEqual(account.available_balance, expected_balance)

        # Clean up
        account.delete()

    def test_increase_pending_balance(self):
        account = Account.objects.create(
            name="Buyer Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_LIABILITY,
            internal_type=self.account_type,
            currency=self.currency,
        )

        expected_balance = Money(1000.0, self.currency.code)

        # Test if the available balance increase by 1000 ZAR
        new_balance = account.increase_pending_balance(1000.0)

        account = Account.objects.get(pk=account.pk)
        self.assertEqual(new_balance, expected_balance)
        self.assertEqual(account.pending_balance, expected_balance)

        # Clean up
        account.delete()

    def test_decrease_pending_balance(self):
        account = Account.objects.create(
            name="Buyer Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_LIABILITY,
            internal_type=self.account_type,
            currency=self.currency,
            pending_balance=Decimal(1000),
        )

        expected_balance = Money(0.0, self.currency.code)

        # Test if the available balance increase by 1000 ZAR
        new_balance = account.decrease_pending_balance(1000.0)

        account = Account.objects.get(pk=account.pk)
        self.assertEqual(new_balance, expected_balance)
        self.assertEqual(account.pending_balance, expected_balance)

        # Clean up
        account.delete()


class JournalTestCase(TestCase):
    def test_unicode(self):
        journal = Journal()
        journal.name = "Test Name"

        text = journal.__unicode__()
        self.assertEqual(text, journal.name)


class JournalEntryTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", password="test"
        )
        # Create require data objects
        cls.account_type = AccountType.objects.create(code="TEST", name="Test")
        cls.currency = Currency.objects.create(
            code=BASE_CURRENCY.code,
            name="Rand",
            is_base=True,
            current_rate=Decimal(1.0),
            date=datetime.now(),
        )
        cls.usd = Currency.objects.create(
            code="USD",
            name="US Dollar",
            is_base=False,
            current_rate=Decimal(0.1),
            date=datetime.now(),
        )

        # Create Buyer and Seller accounts
        cls.buyer = Account.objects.create(
            acc_no="111",
            name="Buyer Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_LIABILITY,
            internal_type=cls.account_type,
            currency=cls.currency,
        )
        cls.seller = Account.objects.create(
            acc_no="222",
            name="Seller Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_LIABILITY,
            internal_type=cls.account_type,
            currency=cls.currency,
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
        cls.buyer.delete()
        cls.seller.delete()
        cls.currency.delete()
        cls.usd.delete()
        cls.account_type.delete()
        cls.user.delete()

    def tearDown(self):
        JournalEntryLine.objects.all().delete()
        JournalEntry.objects.all().delete()
        self.buyer.balance = Decimal(0.0)
        self.buyer.available_balance = Decimal(0.0)
        self.buyer.save()
        self.seller.balance = Decimal(0.0)
        self.seller.available_balance = Decimal(0.0)
        self.seller.save()

    def test_unicode(self):
        jnl_entry = JournalEntry()
        jnl_entry.ref_no = "Test Ref"

        text = jnl_entry.__unicode__()
        self.assertEqual(text, jnl_entry.ref_no)

    @patch("account.models.gen_uuid")
    @patch("account.models.datetime")
    def test_save(self, datetime_mock, gen_uuid):
        gen_uuid.return_value = "1234"
        test_date = datetime.now()
        datetime_mock.now.return_value = test_date

        jnl_entry = JournalEntry()
        jnl_entry.name = "Test Entry"
        jnl_entry.journal = self.gen_jnl
        jnl_entry.save()

        assert gen_uuid.called
        assert datetime_mock.now.called
        self.assertEqual(jnl_entry.ref_no, "1234")

    def test_get_debit_lines(self):
        # Create the test entry
        jnl_entry = JournalEntry.objects.create(
            ref_no="TEST", name="Test Entry", journal=self.gen_jnl
        )
        self.assertEqual(jnl_entry.get_debit_lines().count(), 0)

        debit_line = JournalEntryLine.objects.create(
            ref_no="DEBIT",
            debit=5000.00,
            credit=0.0,
            description="Debit Journal Entry",
            account=self.buyer,
            journal_entry=jnl_entry,
        )
        credit_line = JournalEntryLine.objects.create(
            ref_no="CREDIT",
            debit=0.00,
            credit=1000.0,
            description="Credit Journal Entry",
            account=self.seller,
            journal_entry=jnl_entry,
        )

        # Test that all lines returned are of type DEBIT
        for line in jnl_entry.get_debit_lines():
            self.assertEqual(line.line_type, DEBIT)

    def test_get_credit_lines(self):
        # Create the test entry
        jnl_entry = JournalEntry.objects.create(
            ref_no="TEST", name="Test Entry", journal=self.gen_jnl
        )
        self.assertEqual(jnl_entry.get_credit_lines().count(), 0)

        debit_line = JournalEntryLine.objects.create(
            ref_no="DEBIT",
            debit=5000.00,
            credit=0.0,
            description="Debit Journal Entry",
            account=self.buyer,
            journal_entry=jnl_entry,
        )
        credit_line = JournalEntryLine.objects.create(
            ref_no="CREDIT",
            debit=0.00,
            credit=1000.0,
            description="Credit Journal Entry",
            account=self.seller,
            journal_entry=jnl_entry,
        )

        # Test the all line returned are of type CREDIT
        for line in jnl_entry.get_credit_lines():
            self.assertEqual(line.line_type, CREDIT)

    @patch("account.models.JournalEntryLine.post")
    def test_post(self, post_mock):
        # Create the test entry
        jnl_entry = JournalEntry.objects.create(
            ref_no="TEST", name="Test Entry", journal=self.gen_jnl
        )

        # If no entry lines are provided it should raise JournalEntryError
        self.assertRaises(JournalEntryError, jnl_entry.post)

        debit_line = JournalEntryLine.objects.create(
            ref_no="DEBIT",
            debit=Money(5000.0, BASE_CURRENCY.code),
            credit=Money(0.0, BASE_CURRENCY.code),
            description="Debit Journal Entry",
            account=self.buyer,
            journal_entry=jnl_entry,
        )
        credit_line = JournalEntryLine.objects.create(
            ref_no="CREDIT",
            debit=Money(0.0, BASE_CURRENCY.code),
            credit=Money(1000.0, BASE_CURRENCY.code),
            description="Credit Journal Entry",
            account=self.seller,
            journal_entry=jnl_entry,
        )

        # If debit differs from credit it should raise JournalEntryError
        self.assertRaises(JournalEntryError, jnl_entry.post)

        debit_line.debit = Money(1000.0, BASE_CURRENCY.code)
        debit_line.credit = Money(0.0, BASE_CURRENCY.code)
        credit_line.debit = Money(0.0, "USD")
        credit_line.credit = Money(100.0, "USD")

        jnl_entry.entry_lines.all().delete()
        jnl_entry.entry_lines.add(debit_line, credit_line)
        jnl_entry.post()

        self.assertTrue(len(post_mock.mock_calls) == 2)
        assert post_mock.called

        # Journal Entry state should be JOURNAL_ENTRY_POSTED
        self.assertEqual(jnl_entry.state, JOURNAL_ENTRY_POSTED)

    def test_create_transfer(self):
        # Test LIABILITY to LIABILITY
        asset = Account.objects.create(
            acc_no="TRANS-ASSET-ACC",
            name="ASSET Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_ASSET,
            internal_type=self.account_type,
            currency=self.currency,
        )
        usd_asset = Account.objects.create(
            acc_no="TRANS-USD-ASSET-ACC",
            name="ASSET Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_ASSET,
            internal_type=self.account_type,
            currency=self.usd,
        )
        liab = Account.objects.create(
            acc_no="TRANS-LIABILITY-ACC",
            name="LIABILITY Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_LIABILITY,
            internal_type=self.account_type,
            currency=self.currency,
        )
        usd_liab = Account.objects.create(
            acc_no="TRANS-USD-LIABILITY-ACC",
            name="USD LIABILITY Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_LIABILITY,
            internal_type=self.account_type,
            currency=self.usd,
        )
        jnl_entry = JournalEntry.objects.create(
            ref_no="TRANS-TEST", name="Test Entry", journal=self.gen_jnl
        )

        # Test that the entries get created for Asset to Liablity accounts with different currencies
        asset.zero_balances()
        usd_liab.zero_balances()

        lines = jnl_entry.create_transfer(
            from_acc=asset,
            to_acc=usd_liab,
            amount=Money(10000.0, BASE_CURRENCY.code),
            name="TEST Name",
            desc="Test Description",
            return_dict=True,
        )
        self.assertEqual(asset.balance, Money(10000.0, BASE_CURRENCY))
        self.assertEqual(usd_liab.balance, Money(1000.0, "USD"))

        # Test that the entries get created for Liability to Asset accounts with different currencies
        usd_liab.zero_balances()
        asset.zero_balances()

        lines = jnl_entry.create_transfer(
            from_acc=usd_liab,
            to_acc=asset,
            amount=Money(10000.0, BASE_CURRENCY.code),
            name="TEST Name",
            desc="Test Description",
            return_dict=True,
        )
        self.assertEqual(usd_liab.balance, Money(-1000.0, "USD"))
        self.assertEqual(asset.balance, Money(-10000.0, BASE_CURRENCY))

        # Test that entries get created for Asset accounts with different currencies
        asset.zero_balances()
        asset.update_balance(debit=Decimal(10000.0), credit=Decimal(0))

        usd_asset.zero_balances()

        lines = jnl_entry.create_transfer(
            from_acc=asset,
            to_acc=usd_asset,
            amount=Money(10000.0, BASE_CURRENCY.code),
            name="TEST Name",
            desc="Test Description",
            return_dict=True,
        )
        self.assertEqual(asset.balance, Money(0, BASE_CURRENCY))
        self.assertEqual(usd_asset.balance, Money(1000.0, "USD"))

        # Test that entries get create for Liability accounts with different currencies
        liab.zero_balances()
        liab.update_balance(debit=Decimal(0), credit=Decimal(10000.0))

        usd_liab.zero_balances()

        lines = jnl_entry.create_transfer(
            from_acc=liab,
            to_acc=usd_liab,
            amount=Money(10000.0, BASE_CURRENCY.code),
            name="TEST Name",
            desc="Test Description",
            return_dict=True,
        )
        self.assertEqual(liab.balance, Money(0, BASE_CURRENCY))
        self.assertEqual(usd_liab.balance, Money(1000.0, "USD"))

        # Test with Decimal amount
        liab.zero_balances()
        liab.update_balance(debit=Decimal(0), credit=Decimal(10000.0))

        usd_liab.zero_balances()

        lines = jnl_entry.create_transfer(
            from_acc=liab,
            to_acc=usd_liab,
            amount=Decimal(10000.0),
            name="TEST Name",
            desc="Test Description",
            return_dict=True,
        )
        self.assertEqual(liab.balance, Money(0, BASE_CURRENCY))
        self.assertEqual(usd_liab.balance, Money(1000.0, "USD"))

        # Clean up
        jnl_entry.delete()
        asset.delete()
        usd_asset.delete()
        liab.delete()
        usd_liab.delete()

    @patch("account.models.JournalEntryLine.post")
    def test_create_balanced_entry(self, post_mock):
        # Test LIABILITY to ASSET
        asset = Account.objects.create(
            acc_no="ASSET-ACC",
            name="ASSET Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_ASSET,
            internal_type=self.account_type,
            currency=self.currency,
        )
        liab = Account.objects.create(
            acc_no="LIABILITY-ACC",
            name="LIABILITY Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_LIABILITY,
            internal_type=self.account_type,
            currency=self.currency,
        )
        usd_liab = Account.objects.create(
            acc_no="USD-LIABILITY-ACC",
            name="USD LIABILITY Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_LIABILITY,
            internal_type=self.account_type,
            currency=self.usd,
        )
        jnl_entry = JournalEntry.objects.create(
            ref_no="TEST", name="Test Entry", journal=self.gen_jnl
        )

        # Raises TypeError if the given accounts are not of type Account
        self.assertRaises(
            TypeError,
            jnl_entry.create_balanced_entry,
            debit_acc=None,
            credit_acc=liab,
            amount=Money(10000.0, BASE_CURRENCY.code),
            name="TEST-Desc",
        )
        self.assertRaises(
            TypeError,
            jnl_entry.create_balanced_entry,
            debit_acc=asset,
            credit_acc=None,
            amount=Money(10000.0, BASE_CURRENCY.code),
            name="TEST-Desc",
        )

        # Raises TypeError if the given amount is not of type Money
        self.assertRaises(
            TypeError,
            jnl_entry.create_balanced_entry,
            debit_acc=asset,
            credit_acc=liab,
            amount=Decimal(10000.0),
            name="TEST-Desc",
        )

        # Raises JournalEntryError if the debit/credit account is the same
        self.assertRaises(
            JournalEntryError,
            jnl_entry.create_balanced_entry,
            debit_acc=liab,
            credit_acc=liab,
            amount=Money(10000.0, BASE_CURRENCY),
            name="TEST-Desc",
        )

        # Test the default name and description
        jnl_entry.create_balanced_entry(
            debit_acc=asset,
            credit_acc=liab,
            amount=Money(10000.0, BASE_CURRENCY.code),
        )

        debit_line = jnl_entry.get_debit_lines()[0]
        self.assertEqual(debit_line.name, "#DEBIT")
        self.assertEqual(debit_line.description, "'ASSET-ACC' debited.")

        credit_line = jnl_entry.get_credit_lines()[0]
        self.assertEqual(credit_line.name, "#CREDIT")
        self.assertEqual(credit_line.description, "'LIABILITY-ACC' credited.")

        debit_line.delete()
        credit_line.delete()

        # Test a name and description list
        jnl_entry.create_balanced_entry(
            debit_acc=asset,
            credit_acc=liab,
            amount=Money(10000.0, BASE_CURRENCY.code),
            name="TEST",
            desc=["Debit description", "Credit description"],
        )

        debit_line = jnl_entry.get_debit_lines()[0]
        self.assertEqual(debit_line.name, "TEST")
        self.assertEqual(debit_line.description, "Debit description")

        credit_line = jnl_entry.get_credit_lines()[0]
        self.assertEqual(credit_line.name, "TEST")
        self.assertEqual(credit_line.description, "Credit description")

        debit_line.delete()
        credit_line.delete()

        # Test a name and a description string with a dollar account
        post_mock.mock_calls = []
        post_mock.called = None
        jnl_entry.state = "NONE"

        asset.zero_balances()
        usd_liab.zero_balances()

        lines = jnl_entry.create_balanced_entry(
            debit_acc=asset,
            credit_acc=usd_liab,
            amount=Money(10000.0, BASE_CURRENCY.code),
            name="TEST",
            desc="Description",
            return_dict=True,
        )

        debit_line = jnl_entry.get_debit_lines()[0]
        self.assertEqual(debit_line.name, "TEST")
        self.assertEqual(debit_line.description, "Description")

        credit_line = jnl_entry.get_credit_lines()[0]
        self.assertEqual(credit_line.name, "TEST")
        self.assertEqual(credit_line.description, "Description")

        self.assertTrue(len(post_mock.mock_calls) == 2)
        assert post_mock.called

        self.assertEqual(jnl_entry.state, JOURNAL_ENTRY_POSTED)

        self.assertEqual(lines[DEBIT].id, debit_line.id)
        self.assertEqual(lines[CREDIT].id, credit_line.id)

        self.assertEqual(debit_line.debit.amount, 10000.0)

        # We entered R10,000.00 which is $1,000.0
        self.assertEqual(credit_line.credit.amount, 1000.0)

        # Clean up
        jnl_entry.delete()
        debit_line.delete()
        credit_line.delete()
        asset.delete()
        liab.delete()
        usd_liab.delete()

    def test_add_debit_line(self):
        asset = Account.objects.create(
            acc_no="ASSET-ACC",
            name="ASSET Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_ASSET,
            internal_type=self.account_type,
            currency=self.currency,
        )
        jnl_entry = JournalEntry.objects.create(
            ref_no="TEST", name="Test Entry", journal=self.gen_jnl
        )

        # Should Raise TypeError if the given account is not of type Account
        self.assertRaises(
            TypeError,
            jnl_entry.add_debit_line,
            debit_acc=None,
            amount=Money(100.0, BASE_CURRENCY.code),
            date_created=datetime.now(),
            name="TEST",
        )

        # Test with no description and Money amount
        debit_line = jnl_entry.add_debit_line(
            debit_acc=asset,
            amount=Money(100.0, BASE_CURRENCY.code),
            date_created=datetime.now(),
            name="TEST",
        )

        self.assertEqual(debit_line.description, "'ASSET-ACC' debited.")
        self.assertEqual(debit_line.debit, Money(100.0, BASE_CURRENCY.code))
        self.assertEqual(debit_line.credit, Money(0.0, BASE_CURRENCY.code))
        debit_line.delete()

        # Test with description and float amount
        debit_line = jnl_entry.add_debit_line(
            debit_acc=asset,
            amount=100.0,
            date_created=datetime.now(),
            name="TEST",
            desc="Description",
        )

        self.assertEqual(debit_line.description, "Description")
        self.assertEqual(debit_line.debit, Money(100.0, BASE_CURRENCY.code))
        self.assertEqual(debit_line.credit, Money(0.0, BASE_CURRENCY.code))

        jnl_debit_line = jnl_entry.get_debit_lines()[0]
        self.assertEqual(jnl_debit_line.id, debit_line.id)
        debit_line.delete()

        asset.delete()
        jnl_entry.delete()

    def test_add_credit_line(self):
        asset = Account.objects.create(
            acc_no="ASSET-ACC",
            name="ASSET Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_ASSET,
            internal_type=self.account_type,
            currency=self.currency,
        )
        jnl_entry = JournalEntry.objects.create(
            ref_no="TEST", name="Test Entry", journal=self.gen_jnl
        )

        # Should Raise TypeError if the given account is not of type Account
        self.assertRaises(
            TypeError,
            jnl_entry.add_credit_line,
            credit_acc=None,
            amount=Money(100.0, BASE_CURRENCY.code),
            date_created=datetime.now(),
            name="TEST",
        )

        # Test with no description and Money amount
        credit_line = jnl_entry.add_credit_line(
            credit_acc=asset,
            amount=Money(100.0, BASE_CURRENCY.code),
            date_created=datetime.now(),
            name="TEST",
        )

        self.assertEqual(credit_line.description, "'ASSET-ACC' credited.")
        self.assertEqual(credit_line.debit, Money(0.0, BASE_CURRENCY.code))
        self.assertEqual(credit_line.credit, Money(100.0, BASE_CURRENCY.code))
        credit_line.delete()

        # Test with description and float amount
        credit_line = jnl_entry.add_credit_line(
            credit_acc=asset,
            amount=100.0,
            date_created=datetime.now(),
            name="TEST",
            desc="Description",
        )

        self.assertEqual(credit_line.description, "Description")
        self.assertEqual(credit_line.debit, Money(0.0, BASE_CURRENCY.code))
        self.assertEqual(credit_line.credit, Money(100.0, BASE_CURRENCY.code))

        jnl_credit_line = jnl_entry.get_credit_lines()[0]
        self.assertEqual(jnl_credit_line.id, credit_line.id)
        credit_line.delete()

        asset.delete()
        jnl_entry.delete()

    @patch("account.models.JournalEntryLine.reconcile_line")
    def test_reconcile_entry(self, reconcile_line):
        asset = Account.objects.create(
            acc_no="ASSET-ACC",
            name="ASSET Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_ASSET,
            internal_type=self.account_type,
            currency=self.currency,
        )
        jnl_entry = JournalEntry.objects.create(
            ref_no="TEST", name="Test Entry", journal=self.gen_jnl
        )

        # Should raise an AccountError if the reconcile_type is incorrect
        self.assertRaises(
            AccountError, jnl_entry.reconcile_entry, reconcile_type="NONE"
        )

        credit_line = jnl_entry.add_credit_line(
            credit_acc=asset,
            amount=0.0,
            date_created=datetime.now(),
            name="TEST",
            desc="Description",
        )
        Reconcile.objects.all().delete()

        jnl_entry.reconcile_entry(reconcile_type=RECONCILE_GENERAL)

        reconcile = Reconcile.objects.filter(
            reconcile_type=RECONCILE_GENERAL
        ).first()
        assert reconcile_line.called
        self.assertTrue(reconcile)

        # Delete all db objects
        credit_line.delete()
        asset.delete()
        jnl_entry.delete()
        Reconcile.objects.all().delete()

    @patch("account.models.JournalEntry.reconcile_entry")
    def test_bank_reconcile_entry(self, reconcile_entry):
        jnl_entry = JournalEntry()

        jnl_entry.bank_reconcile_entry()

        reconcile_entry.assert_called_with(RECONCILE_BANK)


class JournalEntryLineTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", password="test"
        )
        # Create require data objects
        cls.account_type = AccountType.objects.create(code="TEST", name="Test")
        cls.currency = Currency.objects.create(
            code=BASE_CURRENCY.code,
            name="Rand",
            is_base=True,
            current_rate=1.0,
            date=datetime.now(),
        )

        # Create Buyer and Seller accounts
        cls.buyer = Account.objects.create(
            acc_no="111",
            name="Buyer Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_LIABILITY,
            debit=0.0,
            credit=0.0,
            balance=0.0,
            internal_type=cls.account_type,
            currency=cls.currency,
        )
        cls.seller = Account.objects.create(
            acc_no="222",
            name="Seller Account",
            date_created=datetime.now(),
            accounting_type=ACCOUNT_LIABILITY,
            debit=0.0,
            credit=0.0,
            balance=0.0,
            internal_type=cls.account_type,
            currency=cls.currency,
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
        cls.buyer.delete()
        cls.seller.delete()
        cls.currency.delete()
        cls.account_type.delete()
        cls.user.delete()

    def tearDown(self):
        JournalEntryLine.objects.all().delete()
        JournalEntry.objects.all().delete()
        self.buyer.balance = 0.0
        self.buyer.save()
        self.seller.balance = 0.0
        self.seller.save()

    def test_unicode(self):
        line = JournalEntryLine()
        line.ref_no = "Test Ref"

        text = line.__unicode__()
        self.assertEqual(text, line.ref_no)

    def test_set_debit(self):
        line = JournalEntryLine()

        line.set_debit(Money(1000.0, BASE_CURRENCY.code))

        self.assertEqual(line.debit, Money(1000.0, BASE_CURRENCY.code))
        self.assertEqual(line.credit, Money(0.0, BASE_CURRENCY.code))
        self.assertEqual(line.line_type, DEBIT)

    def test_set_credit(self):
        line = JournalEntryLine()

        line.set_credit(Money(1000.0, BASE_CURRENCY.code))

        self.assertEqual(line.debit, Money(0.0, BASE_CURRENCY.code))
        self.assertEqual(line.credit, Money(1000.0, BASE_CURRENCY.code))
        self.assertEqual(line.line_type, CREDIT)

    @patch("account.models.Account.update_balance")
    def test_post(self, update_balance):
        update_balance.return_value = Decimal(5000.0)

        # Create the test entry
        jnl_entry = JournalEntry.objects.create(
            ref_no="TEST", name="Test Entry", journal=self.gen_jnl
        )

        debit_line = JournalEntryLine.objects.create(
            ref_no="DEBIT",
            debit=Money(5000.0, BASE_CURRENCY.code),
            credit=Money(0.0, BASE_CURRENCY.code),
            description="Debit Journal Entry",
            account=self.buyer,
            journal_entry=jnl_entry,
        )

        # JournalEntryLine state should be UNPOSTED
        self.assertEqual(debit_line.state, JOURNAL_ENTRY_LINE_UNPOSTED)

        # Should raise JournalEntryLineError if state is JOURNAL_ENTRY_LINE_POSTED
        debit_line.state = JOURNAL_ENTRY_LINE_POSTED

        self.assertRaises(JournalEntryLineError, debit_line.post)

        # JournalEntryLine state should be POSTED
        debit_line.state = JOURNAL_ENTRY_LINE_UNPOSTED
        debit_line.post()

        update_balance.assert_called_with(
            debit=Money(5000.0, BASE_CURRENCY.code),
            credit=Money(0.0, BASE_CURRENCY.code),
        )
        self.assertEqual(debit_line.state, JOURNAL_ENTRY_LINE_POSTED)
        self.assertEqual(
            debit_line.account_balance, Money(5000.0, BASE_CURRENCY.code)
        )

        # Clean up
        debit_line.delete()
        jnl_entry.delete()

    def test_reconcile_line(self):
        line = JournalEntryLine()
        line.save = MagicMock(name="save")

        # Should raise TypeError if the given reconcile is not of type Reconcile
        self.assertRaises(TypeError, line.reconcile_line, None)

        recon = Reconcile()
        recon.ref_no = "1234"
        recon.reconcile_type = RECONCILE_BANK
        recon.date_created = datetime.now()

        line.reconcile_line(recon)

        self.assertEqual(line.state, JOURNAL_ENTRY_LINE_RECONCILE)
        assert line.save.called

    def test_statement_amount(self):
        line = JournalEntryLine()
        line.line_type = DEBIT
        line.debit = Money(1000, self.currency.code)
        line.credit = Money(0, self.currency.code)

        # Should return -1 * line.debit
        amount = line.statement_amount
        self.assertEqual(amount, -1 * line.debit)

        # Should return credit
        line.line_type = CREDIT
        amount = line.statement_amount
        self.assertEqual(amount, line.credit)

    def test_save(self):
        # Create the test entry
        jnl_entry = JournalEntry.objects.create(
            ref_no="TEST", name="Test Entry", journal=self.gen_jnl
        )

        line = JournalEntryLine.objects.create(
            ref_no="DEBIT",
            debit=5000.00,
            credit=0.0,
            description="Debit Journal Entry",
            account=self.buyer,
            journal_entry=jnl_entry,
        )
        line.save()

        # Line type should be DEBIT
        self.assertEqual(line.line_type, DEBIT)

        line.line_type = "N"
        line.debit = 0.0
        line.credit = 5000.0
        line.save()
        # Line type should be CREDIT
        self.assertEqual(line.line_type, CREDIT)

        line.line_type = "N"
        line.debit = 5000.0
        line.credit = 5000.0
        # If line has both a debit and credit value and type of 'N' it should raise
        # JournalEntryLineError
        self.assertRaises(JournalEntryLineError, line.save)

        line.line_type = DEBIT
        # If line has both a debit and credit value and a valid DEBIT/CREDIT type
        # it should raise a JournalEntryLineError
        self.assertRaises(JournalEntryLineError, line.save)


class ReconcileTestCase(TestCase):
    def test_unicode(self):
        recon = Reconcile()
        recon.ref_no = "Test Ref"

        text = recon.__unicode__()
        self.assertEqual(text, recon.ref_no)

    @patch("account.models.datetime")
    @patch("account.models.random")
    @patch("django.db.models.base.Model.save")
    @patch("account.models.luhn_sign")
    @patch("account.models.gen_feistel")
    @patch("account.models.connection")
    def test_save(
        self, connection, gen_feistel, luhn_sign, save, random, datetime
    ):
        # Configure mocks
        cursor_mock = MagicMock(name="cursor")

        connection.cursor.return_value = cursor_mock

        random.randint.return_value = 1000

        date_mock = MagicMock(name="date")
        date_mock.strftime.return_value = "20140101"
        datetime.now.return_value = date_mock

        gen_feistel.return_value = 1000
        luhn_sign.return_value = 1000

        n = int("20140101" + "1000")

        recon = Reconcile()
        recon.reconcile_type = RECONCILE_BANK

        # Test with db vendor == 'sqlite'
        cursor_mock.db.vendor = "sqlite"

        recon.save()

        assert save.called
        random.randint.assert_called_with(0, 100000)
        assert datetime.now.called
        date_mock.strftime.assert_called_with("%Y%m%d")
        gen_feistel.assert_called_with(n)
        luhn_sign.assert_called_with(1000)
        self.assertEqual(recon.ref_no, "RECON-1000")

        # Test with db vendor == 'postgres'
        cursor_mock.db.vendor = "postgres"
        cursor_mock.fetchone.return_value = [1000]
        save.called = None

        recon.ref_no = None
        recon.save()

        assert save.called
        assert connection.cursor.called
        cursor_mock.execute.assert_called_with(
            "SELECT nextval('account_reconcile_id_seq')"
        )
        assert cursor_mock.fetchone.called
        assert datetime.now.called
        date_mock.strftime.assert_called_with("%Y%m%d")
        gen_feistel.assert_called_with(n)
        luhn_sign.assert_called_with(1000)
        self.assertEqual(recon.ref_no, "RECON-1000")
