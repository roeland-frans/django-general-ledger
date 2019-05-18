from base.mixins import PermittedMixin
from django.test import TestCase
from mock import MagicMock


class PermittedMixinTestCase(TestCase):
    def test_for_user(self):
        perm_mock = MagicMock(name="perm")

        perm = PermittedMixin
        perm.objects = []
        perm.temp_func = perm.permitted_filter
        perm.permitted_filter = perm_mock

        perm.for_user("user")
        perm.permitted_filter = perm.temp_func

        perm_mock.assert_called_with(queryset=perm.objects, user="user")

    def test_permitted_filter(self):
        self.assertRaises(
            NotImplementedError, PermittedMixin.permitted_filter, [], "user"
        )
