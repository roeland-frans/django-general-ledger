from base.generate_no import digits_of
from base.generate_no import feistel_generator
from base.generate_no import gen_feistel
from base.generate_no import gen_uuid
from base.generate_no import is_luhn_valid
from base.generate_no import luhn_checksum
from base.generate_no import luhn_sign
from base.generate_no import sample_f
from base.generate_no import sum2digits
from mock import MagicMock
from mock import patch
from unittest import TestCase


class GenerateNoTestCase(TestCase):
    def test_sample_f(self):
        x = 5.6
        y = int((((1366 * x + 150889) % 714025) * 32767) // 714025)

        num = sample_f(x)

        self.assertEqual(num, y)

    def test_luhn_checksum(self):
        y = luhn_checksum(1788827948)
        self.assertEqual(y, 0)

        y = luhn_checksum(573852158)
        self.assertEqual(y, 1)

        y = luhn_checksum(123456789)
        self.assertEqual(y, 7)

    def test_luhn_sign(self):
        y = luhn_sign(78482748)
        self.assertEqual(y, 784827487)

        y = luhn_sign(47380210)
        self.assertEqual(y, 473802106)

        y = luhn_sign(123456789)
        self.assertEqual(y, 1234567897)

    def test_is_luhn_valid(self):
        result = is_luhn_valid(1234567897)
        self.assertTrue(result)

        result = is_luhn_valid(473802106)
        self.assertTrue(result)

        result = is_luhn_valid(34518893)
        self.assertFalse(result)

    def test_digits_of(self):
        num_list = digits_of(1234)

        self.assertEqual(num_list, [1, 2, 3, 4])

    def test_sum2digits(self):
        x = 17
        y = (x // 10) + (x % 10)

        num = sum2digits(x)

        self.assertEqual(num, y)

    @patch("base.generate_no.make_feistel_number")
    def test_feistel_generator(self, make_feistel_number):
        make_feistel_number.return_value = "feistel"

        feistel_gen = feistel_generator()

        self.assertEqual(feistel_gen, "feistel")
        make_feistel_number.assert_called_with(sample_f)

    @patch("uuid.uuid4")
    def test_gen_uuid(self, uuid4):
        uuid4.return_value = "1234"

        result = gen_uuid()

        self.assertEqual(result, "1234")
        assert uuid4.called

    @patch("base.generate_no.feistel_generator")
    def test_gen_feistel(self, feistel_generator):
        feistel_mock = MagicMock(name="feistel")
        feistel_mock.return_value = 1234
        feistel_generator.return_value = feistel_mock

        result = gen_feistel(1)

        self.assertEqual(result, 1234)
        assert feistel_generator.called
        feistel_mock.assert_called_with(1)
