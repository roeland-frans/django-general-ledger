from base.models import UserProfile
from base_testcases import BaseTestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test.client import Client


class LoginViewTestCase(BaseTestCase):
    """
    This test case tests the login of the back office.
    """

    def setUp(self):
        """
        Setup for test.
        """
        User = get_user_model()
        self.client = Client()

        self.normal_user = User.objects.create_user(
            username="test", email="test@tradersvault.co.za", password="pass"
        )
        self.normal_user.is_staff = False
        self.normal_user.is_active = True
        self.normal_user.save()
        self.staff_user = User.objects.create_user(
            username="staff", email="staff@tradersvault.co.za", password="pass"
        )
        self.staff_user.is_staff = True
        self.staff_user.is_active = True
        self.staff_user.save()

        self.normal_profile = UserProfile.objects.create(
            user=self.normal_user, mobile="084WHATUP"
        )
        self.staff_profile = UserProfile.objects.create(
            user=self.staff_user, mobile="082WHATUP"
        )

    def test_login_not_staff(self):
        """
        Tests that only staff members are allowed to login to back office.
        """
        # Log in as normal user.
        self.client.post(
            reverse("login"),
            {
                "username": "test",
                "password": "pass",
                "next": reverse("backoffice"),
            },
        )
        response = self.client.get(reverse("backoffice"))
        self.assertEqual(response.status_code, 302)
        # Should redirect to login page.
        self.assertEqual("http://testserver" + reverse("login"), response.url)

        # Log in as staff.
        self.client.post(
            reverse("login"),
            {
                "username": "staff",
                "password": "pass",
                "next": reverse("backoffice"),
            },
        )
        response = self.client.get(reverse("backoffice"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"].username, "staff")
