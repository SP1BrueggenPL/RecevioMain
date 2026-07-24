from background_task import background
from background_task.models import Task
from django.utils import timezone
from datetime import timedelta
from django.core.management import call_command
from .models import Visitor

REMIND_UNPICKED_PACKAGES_TASK_NAME = "GuestBook.task.remind_unpicked_packages_task"
CLOSE_EXPIRED_VISITORS_TASK_NAME = "GuestBook.task.close_expired_visitors_task"


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


def schedule_recurring_tasks():
    """(Re)schedule the repeating background tasks, idempotently.

    Only creates a new Task row when one isn't already pending, so this can be
    called on every app startup / gunicorn worker import without piling up
    duplicate scheduled tasks (each import used to unconditionally create a new
    row, so every deploy/restart added more of them).
    """
    if not Task.objects.filter(task_name=CLOSE_EXPIRED_VISITORS_TASK_NAME).exists():
        close_expired_visitors_task(repeat=3600)
    if not Task.objects.filter(task_name=REMIND_UNPICKED_PACKAGES_TASK_NAME).exists():
        remind_unpicked_packages_task(repeat=3600)
