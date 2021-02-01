import ledger_api.rest_views as rest_views
import ledger_api.views as views

from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"dashboard", rest_views.DashboardView, base_name="dashboard")
router.register(r"users", rest_views.UsersViewSet)
router.register(
    r"users_for_entity",
    rest_views.UsersForEntityViewSet,
    base_name="users_for_entity",
)
router.register(r"user_profiles", rest_views.ProfileViewSet)
router.register(r"entities", rest_views.EntitiesViewSet)
router.register(
    r"entities_for_user",
    rest_views.EntitiesForUserViewSet,
    base_name="entities_for_user",
)
router.register(
    r"account_all", rest_views.AccountViewSet, base_name="account_all"
)
router.register(
    r"account_traders",
    rest_views.AccountTradersViewSet,
    base_name="account_traders",
)
router.register(
    r"account_general",
    rest_views.AccountGeneralViewSet,
    base_name="account_general",
)
router.register(
    r"account_bank", rest_views.AccountBankViewSet, base_name="account_bank"
)
router.register(r"journal_entries", rest_views.JournalEntriesViewSet)

urlpatterns = [
    url(r"^rest/", include(router.urls)),
    url(
        r"^api-auth/",
        include("rest_framework.urls", namespace="rest_framework"),
    ),
    url(
        r"^login/$",
        "django.contrib.auth.views.login",
        {"template_name": "backoffice/login.html"},
        name="login",
    ),
    url(
        r"^logout/$",
        "django.contrib.auth.views.logout",
        {"template_name": "backoffice/logout.html"},
        name="logout",
    ),
    url(r"^admin/", admin.site.urls),
    url(r"^$", views.Backoffice.as_view(), name="backoffice"),
]
