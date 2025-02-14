"""Item Auth forms."""

import logging

from django_recaptcha.fields import ReCaptchaField
from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.template import loader

from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from apps.dictation_auth.models import User

from apps.dictation_auth.utils import CustomEmailMessage
from apps.dictation_auth.widget import CustomReCaptchaV3

UserModel = get_user_model()
logger = logging.getLogger("django.contrib.auth")


class UserCreationForm(auth_forms.UserCreationForm):
    """User creation form class."""

    class Meta(auth_forms.UserCreationForm.Meta):
        """User creation form meta class."""

        model = get_user_model()


class SignupForm(auth_forms.UserCreationForm):
    """Signup form."""

    def __init__(self, *args, **kwargs):
        csp_nonce = kwargs.pop("csp_nonce", None)
        super().__init__(*args, **kwargs)
        self.fields["captcha"].widget.attrs["csp_nonce"] = csp_nonce

    email = forms.CharField(
        label=_("Email address"),
        max_length=254,
        required=True,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control me-2",
                "input_type": "email",
                "data-email": "",
            }
        ),
    )
    username = forms.CharField(
        label=_("Username"),
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control me-2",
            }
        ),
    )
    password1 = forms.CharField(
        label=_("Password"),
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control me-2",
                "input_type": "password",
                "autocomplete": "password1",
            }
        ),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control me-2",
                "input_type": "password",
                "autocomplete": "password2",
            }
        ),
    )

    captcha = ReCaptchaField(widget=CustomReCaptchaV3(action="signup"))

    class Meta:
        """InscriptForm meta class."""

        model = get_user_model()
        fields = ("username", "email", "password1", "password2", "captcha")


class LoginForm(auth_forms.UserCreationForm):
    """Login form."""

    def __init__(self, *args, **kwargs):
        """Init."""
        csp_nonce = kwargs.pop("csp_nonce", None)
        super().__init__(*args, **kwargs)
        self.fields["captcha"].widget.attrs["csp_nonce"] = csp_nonce

        self.invalid_login = ""
        for field in self.fields.values():
            field.error_messages = {
                "required": _("The {fieldname} field is required.").format(
                    fieldname=field.label
                ),
                "invalid_login": _("Please enter a correct email and password."),
            }

        self.invalid_login = [field.error_messages for field in self.fields.values()][
            0
        ]["invalid_login"]

    email = forms.EmailField(
        label=_("Email"),
        max_length=200,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control me-2",
                "placeholder": _(""),
                "data-email": "",
                "autocomplete": "email",
            }
        ),
    )

    captcha = ReCaptchaField(widget=CustomReCaptchaV3(action="login"))

    password = forms.CharField(
        label=_("Password"),
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control me-2",
                "placeholder": "",
                "autocomplete": "current-password",
            }
        ),
    )

    class Meta:
        """LoginForm meta class."""

        model = get_user_model()
        fields = ("email", "password", "captcha")

    def clean(self):
        """Clean."""
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if (
            not self._meta.model.objects.filter(email__iexact=email)
            or not password
            or len(password) < 8
        ):
            raise forms.ValidationError(self.invalid_login)
        elif email and self._meta.model.objects.filter(email__iexact=email).exists():
            pass
        else:
            return email


class CustomPasswordResetForm(PasswordResetForm):
    """Custom password reset form."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)

    email = forms.EmailField(
        label="email",
        widget=forms.EmailInput(
            attrs={"class": "form-control me-2", "type": "email", "name": "email"}
        ),
    )

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = CustomEmailMessage(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        try:
            email_message.send()
        except Exception:
            logger.exception(
                "Failed to send password reset email to %s", context["user"].pk
            )


class CustomSetPasswordForm(SetPasswordForm):
    """Custom set password form."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control me-2", "autocomplete": "new-password"}
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control me-2", "autocomplete": "new-password"}
        ),
    )


class UpdateProfileForm(forms.ModelForm):
    """Update profile form."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)

    username = forms.CharField(
        label=_("Username"),
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control me-2 w-un-250",
            }
        ),
    )

    class Meta:
        """Meta."""

        model = User
        fields = ["username"]


class CustomPasswordChangeForm(SetPasswordForm):
    """Custom password change form."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)

    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control me-2 w-un-250",
                "autocomplete": "current-password",
                "autofocus": True,
            }
        ),
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control me-2 w-un-250",
                "autocomplete": "new-password",
            }
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control me-2 w-un-250",
                "autocomplete": "new-password",
            }
        ),
    )
