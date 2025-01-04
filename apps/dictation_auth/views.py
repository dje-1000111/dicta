"""Dictation auth views."""

import os
import time
from typing import Any, Dict
from smtplib import SMTPDataError
from dotenv import load_dotenv, find_dotenv  # type: ignore

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignupForm, LoginForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
)
from django.contrib.messages.views import SuccessMessageMixin

from apps.dictation_auth.models import User
from apps.dictation_auth.forms import (
    UpdateProfileForm,
    CustomPasswordChangeForm,
)
from apps.dictation_auth.utils import account_activation_token, send_custom_email
from config import settings

load_dotenv(find_dotenv())


def login(request):
    """Login view."""
    if request.method == "POST":
        form = LoginForm(request.POST, csp_nonce=request.csp_nonce)
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user:
            auth_login(
                request, user, backend="django.contrib.auth.backends.ModelBackend"
            )
            return redirect("dictation:home")
    else:
        form = LoginForm(csp_nonce=request.csp_nonce)
    return render(request, "registration/login.html", {"form": form})


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST, csp_nonce=request.csp_nonce)
        if form.is_valid():
            user = form.save(commit=False)
            # Deactivate the user until email confirmation
            user.is_active = False
            user.save()

            # Send email confirmation
            current_site = get_current_site(request)
            subject = "Activate your account"
            from_email = os.getenv("DJANGO_DEFAULT_FROM_EMAIL")
            recipient_list = [user.email]
            message = render_to_string(
                "registration/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )

            try:
                send_custom_email(subject, message, from_email, recipient_list)
            except SMTPDataError:
                # Implement a backoff strategy
                for i in range(3):  # Retry up to 3 times
                    time.sleep(2**i)  # Exponential backoff
                    try:
                        send_custom_email(subject, message, from_email, recipient_list)
                        break  # Exit loop if successful
                    except SMTPDataError:
                        continue  # Try again if it fails

            messages.info(
                request,
                mark_safe(
                    "An activation link has been sent to your email address.<br>\
                        Please check your inbox and click the activation link to activate your account.",
                ),
            )

            return redirect("auth:signup")
    else:
        form = SignupForm(csp_nonce=request.csp_nonce)
    return render(request, "registration/signup.html", {"form": form})


@login_required
def account_activation_sent(request):
    return render(request, "auth:account_activation_sent.html")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        auth_login(
            request, user, backend="apps.dictation_auth.authenticate.EmailModelBackend"
        )
        messages.success(
            request,
            mark_safe(
                f"Welcome, {user.username}! You have successfully activated your account and logged in!"
            ),
        )
        return redirect("auth:profile")
    else:
        messages.info(
            request,
            mark_safe(
                "Activation link is invalid! Please verify your email.",
            ),
        )
        return redirect("auth:signup")


@login_required
def account_activation_complete(request):
    return render(request, "registration/account_activation_complete.html")


@login_required
def profile(request):
    return render(request, "registration/profile.html")


class ProfileView(LoginRequiredMixin, FormView):
    """Profile view."""

    template_name: str = "registration/profile.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Get context data."""
        context = super().get_context_data(**kwargs)

        return context


class UpdateProfile(SuccessMessageMixin, LoginRequiredMixin, FormView):
    initial = {}
    form_class = UpdateProfileForm
    template_name: str = "registration/profile_form.html"
    model = User
    success_message = "Your username: %(username)s was updated successfully"

    # LoginRequiredMixin
    redirect_field_name = settings.LOGIN_URL
    login_url = settings.LOGIN_URL

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            User.objects.filter(pk=self.request.user.pk).update(
                username=form.instance.username
            )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data)

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        initial = super().get_initial()
        initial["username"] = self.request.user.username
        return initial

    def get_success_url(self) -> str:
        """Get success url."""
        return reverse("auth:profile")


@login_required
def delete_account(request):
    """Lead to a confirmation page."""
    return render(request, "registration/delete_account.html")


@login_required
def delete_account_confirm(request):
    """Delete account confirmation."""
    try:
        user = User.objects.get(pk=request.user.pk)
    except (TypeError, ValueError, User.DoesNotExist):
        user = None
    if user is not None:
        user.delete()
        messages.success(
            request,
            mark_safe("Your account has been deleted as well as your datas."),
        )
        return redirect("dictation:home")
    else:
        messages.warning(
            request,
            mark_safe("Permission denied."),
        )
    return render(request, "registration/delete_account.html")


def user_logout(request):
    """Log out."""
    logout(request)
    return redirect("dictation:home")


class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "registration/password_change.html"
    success_url = reverse_lazy("auth:profile")
    success_message = "Your password was changed successfully."

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data)


class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = "registration/password_reset.html"
    email_template_name = "registration/password_reset_email.html"
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("auth:login")
    success_message = mark_safe(
        "We've emailed you instructions for setting your password,\
 if an account exists with the email you entered. You should receive them shortly.<br>\
 If you don't receive an email, please make sure you've entered the address you registered with,\
 and check your spam folder."
    )

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data)


class CustomPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    success_url = reverse_lazy("auth:login")
    success_message = mark_safe("Your new password has been set. You can now Log in")
