from django.core.management.base import BaseCommand
from GuestBook.models import Visitor
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Closes guests who have not returned badges after 8h"

    def handle(self, *args, **kwargs):
        threshold = timezone.now() - timedelta(hours=8)

        visitors_to_close = Visitor.objects.filter(
            end_time__isnull=True,
            badge_returned=False,
            known_guest=True,
            production_area=True,
            approved=True,
            visitor_id__regex=r'^[A-Fa-f0-9]{8}$',  # Tylko HEX
            start_time__lte=threshold
        )

        logger.debug(f"Threshold: {threshold}")
        logger.info(f"Found {visitors_to_close.count()} visitors to close")

        for visitor in visitors_to_close:
            visitor.end_time = timezone.now()
            visitor.save()
            logger.info(f"Closed visit for visitor_id={visitor.visitor_id}")
