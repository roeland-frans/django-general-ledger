from django.core.management.base import BaseCommand
from models import Account


class Command(BaseCommand):
    help = "This will recalculate all the Account balances"

    def handle(self, *args, **options):
        print("Re-calculating account balances")
        accounts = Account.objects.all()
        for acc in accounts:
            acc.zero_balances(False)
            print("Account '%s': %s" % (acc.name, acc.balance))
            entries = acc.account_entry_lines.all().order_by(
                "date_created", "id"
            )
            for entry in entries:
                acc.update_balance(
                    debit=entry.debit, credit=entry.credit, save_acc=False
                )
                entry.account_balance = acc.balance
                entry.save()
                print(
                    "Balance=%s, Id=%s, Entry: %s, Date=%s, debit=%s, credit=%s"
                    % (
                        acc.balance,
                        entry.id,
                        entry.name,
                        entry.date_created,
                        entry.debit,
                        entry.credit,
                    )
                )
            acc.save()
            print("=======================\n")
