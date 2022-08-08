from django.core.exceptions import ObjectDoesNotExist

from .constants import account
from .models import Account


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
