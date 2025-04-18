"""Auth urls."""

from django.urls import path, include

from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetCompleteView,
    PasswordChangeDoneView,
)
from apps.dictation_auth import views
from apps.dictation_auth.forms import CustomSetPasswordForm, CustomPasswordResetForm


auth_patterns = (
    [
        path("accounts/signup/", views.signup, name="signup"),
        path("accounts/login/", views.login, name="login"),
        path("accounts/profile/", views.profile, name="profile"),
        path(
            "accounts/profile/edit",
            views.UpdateProfile.as_view(),
            name="update_profile",
        ),
        path("accounts/signout", views.user_logout, name="signout"),
        path(
            "accounts/profile/delete/",
            views.delete_account,
            name="delete_account",
        ),
        path(
            "accounts/profile/delete-confirm/",
            views.delete_account_confirm,
            name="delete_account_confirm",
        ),
        path(
            "account-activation-sent/",
            views.account_activation_sent,
            name="account_activation_sent",
        ),
        path("activate/<uidb64>/<token>/", views.activate, name="activate"),
        path(
            "activation-complete/",
            views.account_activation_complete,
            name="account_activation_complete",
        ),
        path(
            "password-change/",
            views.CustomPasswordChangeView.as_view(
                template_name="registration/password_change.html"
            ),
            name="profile_password_change",
        ),
    ],
    "auth",
)

urlpatterns = [
    path(
        "accounts/password-change/",
        views.CustomPasswordChangeView.as_view(
            template_name="registration/password_change.html"
        ),
        name="password_change",
    ),
    path(
        "accounts/password-change/done/",
        PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "accounts/password-reset/",
        views.CustomPasswordResetView.as_view(
            template_name="registration/password_reset.html",
            form_class=CustomPasswordResetForm,
        ),
        name="password_reset",
    ),
    path(
        "accounts/password-reset/done/",
        PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "accounts/password-reset-confirm/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            form_class=CustomSetPasswordForm,
        ),
        name="password_reset_confirm",
    ),
    path(
        "accounts/password-reset/complete/",
        PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("", include(auth_patterns)),
]
