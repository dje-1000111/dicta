from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.core.mail import EmailMessage
from email.utils import make_msgid

from config import settings


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Strategy object used to generate and check tokens for the password
    reset mechanism.
    """

    def _make_hash_value(self, user, timestamp):
        """Return a token to confirm email."""
        return f"{text_type(user.pk)}{text_type(timestamp)}{text_type(user.email_confirmed)}"


account_activation_token = AccountActivationTokenGenerator()


class CustomEmailMessage(EmailMessage):
    """Custom email message."""

    def message(self):
        """Return the email message."""
        msg = super().message()
        if "Message-ID" in msg:
            del msg["Message-ID"]
        msg_id = make_msgid(domain=settings.DOMAIN_NAME)
        msg["Message-ID"] = msg_id
        return msg


def send_custom_email(subject, body, from_email, to_list):
    """Send custom email."""
    email = CustomEmailMessage(subject, body, from_email, to_list)
    email.send()
