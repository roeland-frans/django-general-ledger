import base64
import os
import random
import re
import uuid

from base.constants.bank import ENTITY_BANK_ACCOUNT_STATE_UNVERIFIED
from base.constants.bank import ENTITY_BANK_ACCOUNT_STATES
from base.constants.bank import ENTITY_BANK_ACCOUNT_TYPE_CHEQUE_CURRENT
from base.constants.bank import ENTITY_BANK_ACCOUNT_TYPES
from base.constants.entity import ENTITY_INDIVIDUAL
from base.constants.entity import ENTITY_TYPES
from base.generate_no import gen_feistel
from base.generate_no import luhn_sign
from base.mixins import PermittedMixin
from datetime import datetime
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.sessions.models import Session
from django.db import connection
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from pyotp import HOTP

SHA1_RE = re.compile("^[a-f0-9]{40}$")


def rename_avatar_file(instance, filename):
    """
    Renames a profided avatar filename to a unique random filename to avoid info leak and collision on S3.
    @param instance: UserProfile instance for which avatar is being uploaded.
    @param filename: string filename of file being uploaded."""
    filename = "{}.{}".format(uuid.uuid4().hex, filename.split(".")[-1])
    return os.path.join("avatars", filename)


class Address(models.Model):
    """
    This is the database model for an address.
    """

    address = models.CharField(
        _("address"), max_length=100, help_text=_("Your physical address.")
    )
    suburb = models.CharField(_("Suburb"), max_length=100)
    city = models.CharField(_("City"), max_length=100)
    code = models.CharField(_("Postal Code"), max_length=10)
    latitude = models.DecimalField(
        _("GPS Latitude"),
        decimal_places=8,
        max_digits=13,
        blank=True,
        null=True,
    )
    longitude = models.DecimalField(
        _("GPS Longitude"),
        decimal_places=8,
        max_digits=13,
        blank=True,
        null=True,
    )
    country = models.CharField(max_length=16, blank=True, null=True)
    province = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __unicode__(self):
        return "Address: %s, %s, %s" % (
            self.address,
            self.suburb,
            self.country,
        )


class User(AbstractUser):
    @property
    def avatar_url(self):
        """
        Returns an avatar url for the user, which should be either a fully qualified S3 url if an avatar
        thumbnail is available on the user's profile, or otherwise the default root relative avatar.png.

        Handy for user avatar url determination in views, i.e. {{ request.user.avatar_url }}
        """
        return self.get_profile().avatar_url

    def get_profile(self):
        if not hasattr(self, "_profile"):
            self._profile = self.userprofile_set.get()
        return self._profile

    def get_entities(self):
        """
        Returns entities for user.
        """
        return Entity.for_user(user=self).all()

    def get_individual_entity(self):
        """
        Returns entities for user.
        """
        return Entity.for_user(user=self).get(
            entity_type__exact=ENTITY_INDIVIDUAL
        )

    def get_otp(self):
        """
        Generates an OTP for given user and increments user's OTP counter.
        """
        # Get user activity and increment OTP counter.
        # There is potential for a race condition here.
        activity = self.get_activity()

        # Generate a new OTP for the updated counter using combination of
        # global SECRET_KEY and user's password as secret.
        return HOTP(base64.b32encode(settings.SECRET_KEY + self.password)).at(
            activity.otp_counter
        )

    def generate_otp(self):
        """
        Generates an OTP for given user and increments user's OTP counter.
        """
        # Get user activity and increment OTP counter.
        # There is potential for a race condition here.
        activity = self.get_activity()
        activity.otp_counter += 1
        activity.save()

        # Generate a new OTP for the updated counter using combination of
        # global SECRET_KEY and user's password as secret.
        return HOTP(base64.b32encode(settings.SECRET_KEY + self.password)).at(
            activity.otp_counter
        )

    def validate_otp(self, otp):
        """
        Validates a provided OTP against what it should be for this user.

        @param otp int: OTP to validate.
        @return True if the OTP is valid, otherwise a validation error string.
        """
        # Bypass OTP validation when in DEBUG mode, thus allowing for easy dev.
        if settings.DEBUG:
            return True

        # Get user activity containing current OTP counter.
        activity = self.get_activity()

        # Generate an OTP for the current counter using combination of
        # global SECRET_KEY and user's password as secret, and compare
        # against provided otp.
        valid = otp == HOTP(
            base64.b32encode(settings.SECRET_KEY + self.password)
        ).at(activity.otp_counter)

        if valid:
            # Reset invalid counter so as not to affect future OTP entry attempts.
            activity.otp_invalid_counter = 0
            activity.save()
            return True
        else:
            # Increment invalid otp counter.
            activity.otp_invalid_counter += 1
            activity.save()
            if activity.otp_invalid_counter < 7:
                return _("Invalid OTP.")
            elif activity.otp_invalid_counter >= 10:
                # Reset invalid counter so as not to affect future OTP entry attempts.
                activity.otp_invalid_counter = 0
                activity.save()
                # Set profile locked.
                profile = self.get_profile()
                profile.locked = True
                profile.save()
                return _("Invalid OTP. Your account has been locked.")
            else:
                return _(
                    "Invalid OTP. You have {} more attempt(s) before "
                    "your account will be locked.".format(
                        10 - activity.otp_invalid_counter
                    )
                )


# Up username and email field character limits through meta.
# Django doesn't support field overrides of abstract classes by inheriting classes, thus we use this hack, see:
# https://stackoverflow.com/questions/6377631/how-to-override-the-default-value-of-a-model-field-from-an-abstract-base-class
# WARNING: This might very well break if Django internals are changed.
User._meta.get_field("email").max_length = 128
User._meta.get_field("username").max_length = 128


class UserProfile(models.Model):
    """
    This contains all the extra data for a user.

    TODO: Secure
    """

    activation_key = models.CharField(
        _("activation key"), max_length=40, blank=True, null=True
    )
    allow_api_access = models.BooleanField(
        help_text="Select this option to allow the user to access the API.",
        default=False,
    )
    email_secondary = models.EmailField(
        _("Second Email Address (Optional)"), blank=True
    )
    is_affiliate = models.BooleanField(
        help_text="Select this option to indicate the user is an affiliate user.",
        default=False,
    )
    is_partner = models.BooleanField(
        help_text="Select this option to indicate the user is a partner user.",
        default=False,
    )
    mobile = models.CharField(_("Mobile Number"), max_length=15)
    id_no = models.CharField(
        _("ID Number"), max_length=20, blank=True, null=True
    )
    passport_no = models.CharField(
        _("Passport Number"), max_length=20, blank=True, null=True
    )
    passport_country = models.CharField(max_length=16, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    call_count = models.IntegerField(_("Call Count"), default=0)
    login_notifications = models.CharField(
        "Login Notifications",
        max_length=16,
        help_text="Select what method to use for sending login notifications.",
        choices=(("sms", "SMS"), ("email", "Email")),
        default="sms",
    )
    sms_critical = models.BooleanField(
        "SMS Critical Notifications",
        help_text="Select this option if you want to receive critical notifications via SMS.",
        default=True,
    )
    email_critical = models.BooleanField(
        "Email Critical Notifications",
        help_text="Select this option if you want to receive critical notifications via Email.",
        default=True,
    )
    sms_other = models.BooleanField(
        "SMS Other Notifications",
        help_text="Select this option if you want to receive other notifications via SMS.",
        default=False,
    )
    email_other = models.BooleanField(
        "Email Other Notifications",
        help_text="Select this option if you want to receive other notifications via Email.",
        default=True,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar_thumbnail = models.CharField(blank=True, null=True, max_length=250)
    session_key = models.CharField(blank=True, null=True, max_length=40)
    locked = models.BooleanField(
        help_text="Select this option to lock the account which will "
        "suspend it and redirect requests to a user account locked page.",
        default=False,
    )
    origin_ref_no = models.CharField(
        _("Origin Reference"), blank=True, null=True, max_length=50
    )

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def __unicode__(self):
        return self.user.username

    @property
    def avatar_url(self):
        """
        Returns an avatar url for the profile, which should be either a fully qualified S3 url if an avatar
        thumbnail is available on the profile, or otherwise the default root relative avatar.png.
        """
        if self.avatar_thumbnail:
            return self.avatar_thumbnail.url
        else:
            return "{}app/images/avatar.png".format(settings.STATIC_URL)

    def activation_key_expired(self):
        """
        Determine whether this ``RegistrationProfile``'s activation
        key has expired, returning a boolean -- ``True`` if the key
        has expired.

        Key expiration is determined by a two-step process:

        1. If the user has already activated, the key will have been
           removed. Re-activating is not permitted, and so this method returns
           ``True`` in this case.

        2. Otherwise, the date the user signed up is incremented by
           the number of days specified in the setting
           ``ACCOUNT_ACTIVATION_DAYS`` (which should be the number of
           days after signup during which a user is allowed to
           activate their account); if the result is less than or
           equal to the current date, the key has expired and this
           method returns ``True``.

        """
        expiration_date = timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return not self.activation_key or (
            self.user.date_joined + expiration_date <= datetime.now()
        )

    def get_preferred_notification_channels(self):
        """
        Returns a dictionary of channels the user prefers to receive notifications on for
        the various notification classes ('login', 'critical', 'other').
        """
        from notifications.controllers import CHANNEL_EMAIL, CHANNEL_SMS

        result = {"critical": [], "login": [], "other": []}

        # Add channels as determined from profile critical preferences.
        if self.sms_critical:
            result["critical"].append(CHANNEL_SMS)
        if self.email_critical:
            result["critical"].append(CHANNEL_EMAIL)

        # Add channels as determined from profile login preferences.
        if self.login_notifications == "sms":
            result["login"].append(CHANNEL_SMS)
        if self.login_notifications == "email":
            result["login"].append(CHANNEL_EMAIL)

        # Add channels as determined from profile other preferences.
        if self.sms_other:
            result["other"].append(CHANNEL_SMS)
        if self.email_other:
            result["other"].append(CHANNEL_EMAIL)

        return result

    def set_session_key(self, key):
        """
        Update profile's session_key field to the provided key, deleting a session which has the fields current value.
        This is called on login to ensure that each user only has 1 active session at any given time.
        """
        new_session_key = None
        if self.session_key:
            if self.session_key != key:
                try:
                    Session.objects.get(session_key=self.session_key).delete()
                except Session.DoesNotExist:
                    pass
                new_session_key = key
        else:
            new_session_key = key

        if new_session_key is not None:
            self.session_key = new_session_key
            self.save()


class Entity(models.Model, PermittedMixin):
    """
    This is the database model for the an entity.
    An entity is the organisation or individual that will be trading.
    """

    entity_no = models.CharField(
        _("Entity Number"),
        max_length=100,
        unique=True,
        help_text=_("The Entity's Number"),
    )
    entity_type = models.CharField(
        _("Entity Type"),
        max_length=50,
        choices=ENTITY_TYPES,
        help_text=_("Type of entity i.e. Private Individual"),
    )
    name = models.CharField(_("Entity Name"), max_length=200)
    reg_no = models.CharField(
        _("Registration Number"), max_length=50, blank=True
    )
    telephone = models.CharField(_("Telephone Number"), max_length=15)
    fax = models.CharField(_("Fax Number"), max_length=15, blank=True)
    email = models.EmailField(_("E-mail Address"), max_length=128)
    users = models.ManyToManyField(User, related_name="entities")
    physical_address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name="entities_at_physical_address",
        null=True,
    )
    postal_address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name="entities_at_postal_address",
        null=True,
        blank=True,
    )
    bank_verify_count = models.IntegerField(_("Bank Verify Count"), default=0)

    class Meta:
        verbose_name = _("Entity")
        verbose_name_plural = _("Entities")

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.entity_no)

    def save(self, *args, **kwargs):
        """
        Set/check unique generated entity number.
        @todo: implement
        """
        # Generate a unique account number if one does not exist.
        if not self.entity_no:
            if connection.cursor().db.vendor == "sqlite":
                print(
                    "WARNING: SQLITE detected, account number is randomly generated."
                )
                next_id = str(random.randint(0, 100000))
            else:
                cursor = connection.cursor()
                cursor.execute("SELECT nextval('base_entity_id_seq')")
                next_id = str(cursor.fetchone()[0])

            n = int(datetime.now().strftime("%Y%m%d") + next_id)

            self.entity_no = "%09d" % luhn_sign(gen_feistel(n))

        return super(Entity, self).save(*args, **kwargs)

    @classmethod
    def permitted_filter(cls, queryset, user):
        """
        Restricts queryset to only those objects that should be accessible
        by the provided user.

        @param queryset Queryset: queryset to be filtered.
        @param user User: user object for which to filter queryset.
        @return QuerySet: filtered to contain only those objects that should be
            accessible by the provided user.
        """
        return queryset.filter(users=user)


class Bank(models.Model):
    """
    This contains the details of all the Banks that the system can support.
    """

    name = models.CharField(_("Bank Name"), max_length=150)
    validated_name = models.CharField(
        _("Validated Bank Name"), max_length=200, blank=True, null=True
    )
    swift_code = models.CharField(
        _("Bank Swift Code"), max_length=100, blank=True, null=True
    )
    code = models.CharField(_("Bank Code"), max_length=50)
    eft_branch_code = models.CharField(
        _("EFT Branch Code"), max_length=50, blank=True, null=True
    )
    can_verify_accounts = models.BooleanField(
        _("Can Verify Accounts"), default=False
    )

    class Meta:
        verbose_name = _("Bank")
        verbose_name_plural = _("Banks")

    def __unicode__(self):
        return self.name


class EntityBankAccount(models.Model):
    """
    This stores an Entity's bank accounts' details.
    """

    acc_no = models.CharField(_("Bank Acc No"), max_length=100)
    entity = models.ForeignKey(
        Entity, on_delete=models.CASCADE, related_name="bank_accounts"
    )
    bank_account_type = models.CharField(
        _("Bank Account Type"),
        max_length=1,
        choices=ENTITY_BANK_ACCOUNT_TYPES,
        default=ENTITY_BANK_ACCOUNT_TYPE_CHEQUE_CURRENT,
    )
    state = models.CharField(
        _("State"),
        max_length=20,
        choices=ENTITY_BANK_ACCOUNT_STATES,
        default=ENTITY_BANK_ACCOUNT_STATE_UNVERIFIED,
    )
    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name="entity_bank_accounts",
        blank=False,
        null=False,
    )
    bank_name = models.CharField(
        _("Validated Bank Name"), max_length=200, blank=True, null=True
    )
    branch = models.CharField(
        _("Branch Code"), max_length=100, blank=False, null=False
    )

    class Meta:
        verbose_name = _("Entity Bank Account")
        verbose_name_plural = _("Entity Bank Accounts")

    def __unicode__(self):
        return "%s (%s)" % (self.acc_no, self.bank)
