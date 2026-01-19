import requests

from django.core.mail.backends.base import BaseEmailBackend
from config import settings


class CustomEmailBackend(BaseEmailBackend):
    """Custom email backend to send emails via an external service."""

    def send_messages(self, email_messages):
        """Send email messages using an external HTTP service."""
        if not email_messages:
            return 0

        # Construct the URL for the email service
        url = (
            "https://"
            + settings.EMAIL_URL
            + settings.DOMAIN_NAME
            + "/"
            + settings.EMAIL_URL_SUFFIX
        )

        sent_count = 0
        for message in email_messages:
            data = {
                "from": message.from_email,
                "to": message.to,
                "subject": message.subject,
                "text": message.body,
            }
            response = requests.post(
                url, auth=(settings.EMAIL_AUTH, settings.EMAIL_HOST_PASSWORD), data=data
            )
            if response.status_code == 200:
                sent_count += 1
            else:
                print(f"response: {response.status_code} - {response.text}")
        return sent_count
