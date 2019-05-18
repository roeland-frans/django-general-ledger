# /usr/bin/env python
import random
import uuid

from base64 import b32encode
from datetime import date
from datetime import timedelta


def make_feistel_number(f):
    """
    Generate pseudo random consistent reversal number
    per Feistel cypher algorithm.

    see http://en.wikipedia.org/wiki/Feistel_cipher

    >>> feistel_number = make_feistel_number(sample_f)
    >>> feistel_number(1)
    573852158
    >>> feistel_number(2)
    1788827948
    >>> feistel_number(123456789)
    1466105040

    Reversable

    >>> feistel_number(1466105040)
    123456789
    >>> feistel_number(1788827948)
    2
    >>> feistel_number(573852158)
    1
    """

    def feistel_number(n):
        l = (n >> 16) & 65535
        r = n & 65535
        for i in (1, 2, 3):
            l, r = r, l ^ f(r)
        return ((r & 65535) << 16) + l

    return feistel_number


def sample_f(x):
    return int((((1366 * x + 150889) % 714025) * 32767) // 714025)


def luhn_checksum(n):
    """
    Calculates checksum based on Luhn algorithm, also known as
    the "modulus 10" algorithm.

    see http://en.wikipedia.org/wiki/Luhn_algorithm

    >>> luhn_checksum(1788827948)
    0
    >>> luhn_checksum(573852158)
    1
    >>> luhn_checksum(123456789)
    7
    """
    digits = digits_of(n)
    checksum = (
        sum(digits[-2::-2]) + sum(sum2digits(d << 1) for d in digits[-1::-2])
    ) % 10
    return checksum and 10 - checksum or 0


def luhn_sign(n):
    """
    Signs given number by Luhn checksum.

    >>> luhn_sign(78482748)
    784827487
    >>> luhn_sign(47380210)
    473802106
    >>> luhn_sign(123456789)
    1234567897
    """
    return luhn_checksum(n) + (n << 3) + (n << 1)


def is_luhn_valid(n):
    """
    >>> is_luhn_valid(1234567897)
    True
    >>> is_luhn_valid(473802106)
    True
    >>> is_luhn_valid(34518893)
    False
    """
    digits = digits_of(n)
    checksum = sum(digits[-1::-2]) + sum(
        sum2digits(d << 1) for d in digits[-2::-2]
    )
    return checksum % 10 == 0


def digits_of(n):
    """
    Returns a list of all digits from given number.

    >>> digits_of(123456789)
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    return [int(d) for d in str(n)]


def sum2digits(d):
    """
    Sum digits of a number that is less or equal 18.

    >>> sum2digits(2)
    2
    >>> sum2digits(17)
    8
    """
    return (d // 10) + (d % 10)


def feistel_generator():
    """
    Returns a feistel number generator function, note this is not a Python
    Generator.
    """
    return make_feistel_number(sample_f)


def gen_uuid():
    """
    Generate a random UUID.
    """
    return uuid.uuid4()


def gen_feistel(n):
    """
    Generate a feistel number and return the value.
    """
    feistel_number = feistel_generator()
    return feistel_number(n)


def test_feistel():
    """
    Used to test uniqueness of different number formats.
    """
    feistel_number = make_feistel_number(sample_f)
    account_number = lambda n: "Z%011d" % luhn_sign(feistel_number(n))
    human_format = lambda n: "Z%s-%s" % (
        b32encode(chr((n >> 24) & 255) + chr((n >> 16) & 255))[:4],
        b32encode(chr((n >> 8) & 255) + chr(n & 255))[:4],
    )
    return account_number


if __name__ == "__main__":
    counter = 0
    factor = 100000
    limit = factor
    ids = {}

    if_func = test_feistel()
    curr_date = date.today()
    date_str = curr_date.strftime("%Y%m%d")
    date_int = int(date_str)
    day = timedelta(1)

    while 1:
        no_str = date_str + str(counter)
        id = if_func(int(no_str))
        if id in ids:
            print("Duplicate id %s" % id)
            print(
                "Counter: %s, Len Ids: %s, no_str: %s"
                % (counter, len(ids), no_str)
            )
            print("ids[%s] = %s" % (id, ids[id]))
            curr_date += day
            date_str = curr_date.strftime("%Y%m%d")
            counter = 0
        ids[id] = no_str
        counter += 1
        if counter > limit:
            print("Counter reached %s, Len Ids = %s" % (limit, len(ids)))
            limit += factor
            curr_date += day
            date_str = curr_date.strftime("%Y%m%d")
            counter = 0
