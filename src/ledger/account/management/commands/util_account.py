import os

from account.models import Account
from account.models import Journal
from account.models import JournalEntry
from django.core.management.base import BaseCommand
from moneyed.classes import Money


class Command(BaseCommand):
    help = "This is just a test script to test some accounting features."

    def handle(self, *args, **options):
        jnl = Journal.objects.get(code="FNB-TRANS-JNL")
        bank = Account.objects.get(acc_no="62340732545")
        usd = Account.objects.get(acc_no="1234")
        euro = Account.objects.get(acc_no="4321")

        amount = Money(1000.0, "ZAR")

        jnl = Journal.objects.get(code="TRANS-JNL")
        entry = JournalEntry.objects.create(name="Transfer test", journal=jnl)
        entry.create_transfer(from_acc=euro, to_acc=usd, amount=amount)
