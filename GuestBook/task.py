from background_task import background
from django.utils import timezone
from datetime import timedelta
from django.core.management import call_command
from .models import Visitor

@background(schedule=120)
def remind_unpicked_packages_task():
    call_command("remind_unpicked_packages")


@background(schedule=60)
def close_expired_visitors_task():
    threshold = timezone.now() - timedelta(hours=8)
    visitors = Visitor.objects.filter(
        end_time__isnull=True,
        badge_returned=False,
        known_guest=True,
        production_area=True,
        start_time__lte=threshold
    ).filter(visitor_id__regex=r'^[0-9A-Fa-f]{8}$')  # tylko pestka

    print(f"[INFO] Found {visitors.count()} visitors to close")

    for visitor in visitors:
        visitor.end_time = timezone.now()
        visitor.save()
        print(f"[INFO] Auto-closed visitor: {visitor.visitor_id}")
