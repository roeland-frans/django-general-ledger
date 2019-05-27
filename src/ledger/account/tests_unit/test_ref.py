from account.ref import BaseRef
from unittest import TestCase


class BaseRefTestCase(TestCase):
    def test_match_internal_ref(self):
        ref = BaseRef()

        self.assertRaises(NotImplementedError, ref.match_internal_ref, "ref")

    def test_generate(self):
        ref = BaseRef()

        self.assertRaises(NotImplementedError, ref.generate)

    def test_description(self):
        ref = BaseRef()

        self.assertRaises(NotImplementedError, ref.description)
