import bank.constants.bank as bank_constants
import bank.models as bank_models
import base.models as base_models
import datetime
import json
import rest_framework.reverse as rest_reverse

from base_testcases import BaseTestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test.client import Client


class ViewsTestCase(BaseTestCase):
    """
    This tests the views used in the manage views of the back office.
    """

    def setUp(self):
        """
        Create objects.
        """
        User = get_user_model()
        self.client = Client()
        self.test_user = User.objects.create_user(
            username="test@tradersvault.co.za",
            email="test@tradersvault.co.za",
            password="pass",
        )
        self.test_profile = base_models.UserProfile.objects.create(
            user=self.test_user,
            mobile="084WHATUP",
            id_no="8805065115085",
            passport_no="",
            passport_country="SA",
        )
        self.staff_user = User.objects.create_superuser(
            username="staff", email="staff@tradersvault.co.za", password="pass"
        )
        self.staff_profile = base_models.UserProfile.objects.create(
            user=self.staff_user, mobile="082WHATUP"
        )
        # Log in as staff.
        self.client.login(username="staff", password="pass")

    def test_backoffice_view_get(self):
        """
        Ensures that the get function of the view works correctly.
        """
        # Load account search view.
        response = self.client.get(reverse("backoffice"))

        # Check for response.
        self.assertEqual(response.status_code, 200)

    def test_bank_payment_line_edit_action_date(self):
        """
        Ensures that the action date can only be edited when payment
        line state is `UNPOSTED`.
        """
        bank_ref = bank_models.BankPaymentLine.generate_bank_ref()
        ref = bank_ref.internal_ref
        description = bank_ref.description()
        action_date = datetime.datetime.strptime(
            "2015-05-05", "%Y-%m-%d"
        ).date()
        new_action_date = datetime.datetime.strptime(
            "2015-06-06", "%Y-%m-%d"
        ).date()

        payment = bank_models.BankPaymentLine.objects.create(
            action_date=action_date,
            bank_line_type="D",
            amount=100,
            bank_ref=ref,
            description=description,
            debit_account=self.seller_account,
            dest_bank_acc=self.entity_bank_account,
            bank_payment_batch=None,
            state=bank_constants.BANK_LINE_UNPOSTED,
        )

        def post_update_action_date():
            return self.client.patch(
                rest_reverse.reverse(
                    "bank_payment_lines-detail",
                    kwargs={"ref_no": str(payment.ref_no)},
                ),
                data=json.dumps({"action_date": "2015-06-06"}),
                content_type="application/json",
            )

        # Test un-allowed states.
        for state, name in bank_constants.BANK_LINE_STATES_ADMIN:
            if state != bank_constants.BANK_LINE_UNPOSTED:
                payment.state = state
                payment.save()
                response = post_update_action_date()
                payment = bank_models.BankPaymentLine.objects.get(
                    pk=payment.pk
                )
                self.assertEqual(response.status_code, 400)
                self.assertEqual(payment.action_date, action_date)

        # Test `UNPOSTED` state
        payment.state = bank_constants.BANK_LINE_UNPOSTED
        payment.save()
        response = post_update_action_date()
        payment = bank_models.BankPaymentLine.objects.get(pk=payment.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(payment.action_date, new_action_date)

    def test_bank_payment_line_reload_payment(self):
        """
        Ensures that reload payment can only be called when payment
        line state is `ERROR` or `FAILED`.
        """
        bank_ref = bank_models.BankPaymentLine.generate_bank_ref()
        ref = bank_ref.internal_ref
        description = bank_ref.description()
        action_date = datetime.datetime.strptime(
            "2015-05-05", "%Y-%m-%d"
        ).date()
        new_action_date = datetime.datetime.strptime(
            "2015-06-06", "%Y-%m-%d"
        ).date()

        payment = bank_models.BankPaymentLine.objects.create(
            action_date=action_date,
            bank_line_type="D",
            amount=100,
            bank_ref=ref,
            description=description,
            debit_account=self.seller_account,
            dest_bank_acc=self.entity_bank_account,
            bank_payment_batch=None,
            state=bank_constants.BANK_LINE_UNPOSTED,
        )

        count = bank_models.BankPaymentLine.objects.count()

        def post_reload_payment():
            return self.client.post(
                rest_reverse.reverse(
                    "bank_payment_lines-reload-payment",
                    kwargs={"ref_no": str(payment.ref_no)},
                ),
                data=json.dumps({"action_date": "2015-06-06"}),
                content_type="application/json",
            )

        # Test un-allowed states.
        for state, name in bank_constants.BANK_LINE_STATES_ADMIN:
            if (
                state != bank_constants.BANK_LINE_ERROR
                and state != bank_constants.BANK_LINE_FAILED
            ):
                payment.state = state
                payment.save()
                response = post_reload_payment()
                payment = bank_models.BankPaymentLine.objects.get(
                    pk=payment.pk
                )
                self.assertEqual(response.status_code, 400)
                self.assertEqual(payment.state, state)
                self.assertEqual(payment.action_date, action_date)

        # Test `FAILED` state
        payment.state = bank_constants.BANK_LINE_FAILED
        payment.save()
        response = post_reload_payment()
        payment = bank_models.BankPaymentLine.objects.get(pk=payment.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(payment.state, bank_constants.BANK_LINE_RELOADED)
        self.assertEqual(payment.action_date, action_date)
        self.assertEqual(
            bank_models.BankPaymentLine.objects.count(), count + 1
        )
        self.assertEqual(
            bank_models.BankPaymentLine.objects.latest("date_created").state,
            bank_constants.BANK_LINE_UNPOSTED,
        )
        self.assertEqual(
            bank_models.BankPaymentLine.objects.latest(
                "date_created"
            ).action_date,
            new_action_date,
        )

        # Test `FAILED` state
        payment.state = bank_constants.BANK_LINE_FAILED
        payment.save()
        response = post_reload_payment()
        payment = bank_models.BankPaymentLine.objects.get(pk=payment.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(payment.state, bank_constants.BANK_LINE_RELOADED)
        self.assertEqual(payment.action_date, action_date)
        self.assertEqual(
            bank_models.BankPaymentLine.objects.count(), count + 2
        )
        self.assertEqual(
            bank_models.BankPaymentLine.objects.latest("date_created").state,
            bank_constants.BANK_LINE_UNPOSTED,
        )
        self.assertEqual(
            bank_models.BankPaymentLine.objects.latest(
                "date_created"
            ).action_date,
            new_action_date,
        )
