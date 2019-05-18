from base.models import Address
from base.models import Bank
from base.models import Entity
from base.models import EntityBankAccount
from base.models import User
from base.models import UserProfile
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm


class AddressAdmin(admin.ModelAdmin):
    list_display = ("address", "suburb", "city", "province", "country")
    list_filter = ("country", "province")


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "mobile", "id_no", "passport_no")
    search_fields = ["user__username", "id_no", "passport_no", "mobile"]


class EntityAdmin(admin.ModelAdmin):
    list_display = ("entity_no", "name", "entity_type")
    list_filter = ("entity_type",)


class EntityBankAccountAdmin(admin.ModelAdmin):
    list_display = ("acc_no", "state", "bank_account_type", "entity", "bank")
    list_filter = ("bank",)


class BankAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "eft_branch_code", "can_verify_accounts")


class UserProfileInline(admin.options.StackedInline):
    model = UserProfile
    extra = 1


class BaseUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages["duplicate_username"],
            code="duplicate_username",
        )

    def save(self, commit=True):
        user = super(BaseUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class BaseUserAdmin(UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "date_joined",
        "is_staff",
        "is_active",
    )
    add_form = BaseUserCreationForm
    inlines = [UserProfileInline]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(EntityBankAccount, EntityBankAccountAdmin)
admin.site.register(Bank, BankAdmin)
admin.site.register(User, BaseUserAdmin)
