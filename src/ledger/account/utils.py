from account.constants import account
from account.models import Account
from django.core.exceptions import ObjectDoesNotExist


def get_root_account():
    """
    This will return the system user.
    @return: Returns the Account object or False.
    """
    try:
        root_account = Account.objects.get(acc_no=account.ROOT_ACC_NO)
    except ObjectDoesNotExist:
        root_account = False

    return root_account
