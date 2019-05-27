from account.constants.account import ROOT_ACC_NO
from account.utils import get_root_account
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from mock import MagicMock
from mock import patch


class GetRootAccountTestCase(TestCase):
    @patch("account.utils.Account")
    def test_get_root_account(self, Account):
        # Configure mocks
        get_mock = MagicMock(name="get")
        get_mock.return_value = "root_account"

        Account.objects.get = get_mock

        # Test with no exception
        account = get_root_account()

        self.assertEqual(account, "root_account")
        get_mock.assert_called_with(acc_no=ROOT_ACC_NO)

        # Test with ObjectDoesNotExist exception
        get_mock = MagicMock(name="get", side_effect=ObjectDoesNotExist)
        Account.objects.get = get_mock

        account = get_root_account()

        self.assertFalse(account)
        get_mock.assert_called_with(acc_no=ROOT_ACC_NO)
