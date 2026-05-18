import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class MailService:
    def __init__(self):
        self.conn_str = os.environ.get("ACS_CONNECTION_STRING", "")
        self.sender = os.environ.get("ACS_SENDER_ADDRESS", "")
        self.whitelist = os.environ.get("MAIL_WHITELIST_DOMAIN", "")

    def _available(self) -> bool:
        return bool(self.conn_str and self.sender)

    def _validate(self, recipients: list[str], subject: str):
        if not recipients:
            raise ValueError("Brak odbiorcy.")
        for r in recipients:
            if "@" not in r:
                raise ValueError(f"Nieprawidłowy adres: {r}")
            if self.whitelist and not r.lower().endswith(f"@{self.whitelist.lower()}"):
                raise ValueError(f"Domena niedozwolona: {r} (dozwolona: {self.whitelist})")
        if not subject or len(subject) > 255:
            raise ValueError("Temat pusty lub za długi.")

    def send(
        self,
        recipients: list[str],
        subject: str,
        body: str,
        html: bool = False,
        app_user: Optional[str] = None,
    ) -> dict:
        if not self._available():
            raise RuntimeError(
                "ACS_CONNECTION_STRING lub ACS_SENDER_ADDRESS nie są ustawione "
                "w konfiguracji Azure App Service."
            )
        self._validate(recipients, subject)

        from azure.communication.email import EmailClient
        client = EmailClient.from_connection_string(self.conn_str)
        message = {
            "senderAddress": self.sender,
            "recipients": {"to": [{"address": r} for r in recipients]},
            "content": {
                "subject": subject,
                ("html" if html else "plainText"): body,
            },
        }
        poller = client.begin_send(message)
        result = poller.result()
        logger.info("Mail sent by %s to %s, id=%s", app_user, recipients, result.get("id"))
        return {"status": "sent", "message_id": result.get("id")}


_mail_service = MailService()


def send_via_acs(
    email: str,
    subject: str,
    body: str,
    html: bool = False,
    app_user: Optional[str] = None,
) -> str:
    """
    Convenience wrapper matching the old send_email_with_timeout signature.
    Returns 'sent' | 'skipped' | 'error'.
    Falls back to Django SMTP if ACS is not configured.
    """
    if not email:
        return "skipped"

    # Prefer ACS if configured
    if _mail_service._available():
        try:
            _mail_service.send([email], subject, body, html=html, app_user=app_user)
            return "sent"
        except Exception as e:
            logger.exception("[ACS EMAIL ERROR] %s", e)
            return "error"

    # Fallback: Django SMTP backend
    try:
        from django.core.mail import send_mail as _send_mail
        from django.conf import settings as _s
        _send_mail(subject, body, _s.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
        return "sent"
    except Exception as e:
        logger.exception("[SMTP EMAIL ERROR] %s", e)
        return "error"
