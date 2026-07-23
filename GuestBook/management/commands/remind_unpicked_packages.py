from collections import defaultdict
from datetime import timedelta
import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from GuestBook.models import Package
from GuestBook.mail_service import send_pending_package_reminder

logger = logging.getLogger(__name__)

REMINDER_THRESHOLD = timedelta(hours=48)


class Command(BaseCommand):
    help = "E-mails recipients (once) about packages sitting unpicked in the locker for 48h+"

    def handle(self, *args, **kwargs):
        threshold = timezone.now() - REMINDER_THRESHOLD

        packages = list(
            Package.objects.select_related("sender", "recipient").filter(
                status=Package.Status.IN_BOX,
                delivered_at__lte=threshold,
                reminder_sent_at__isnull=True,
            )
        )
        logger.info(f"Found {len(packages)} unpicked package(s) older than 48h")

        by_recipient = defaultdict(list)
        for pkg in packages:
            if getattr(pkg.recipient, "email", None):
                by_recipient[pkg.recipient].append(pkg)

        now = timezone.now()
        for recipient, pkgs in by_recipient.items():
            packages_info = [
                {
                    "code": p.code,
                    "sender": getattr(p.sender, "name", ""),
                    "delivered_at": p.delivered_at,
                    "comment": p.staff_comment,
                }
                for p in pkgs
            ]
            status = send_pending_package_reminder(recipient.email, packages_info)
            logger.info(f"Reminder ({status}) sent to {recipient.email} for {len(pkgs)} package(s)")

            for pkg in pkgs:
                pkg.reminder_sent_at = now
                pkg.save(update_fields=["reminder_sent_at"])
