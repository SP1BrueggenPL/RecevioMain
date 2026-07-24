#!/bin/bash
python manage.py migrate --noinput

# django-background-tasks needs a worker process to actually consume the queue
# (close_expired_visitors_task / remind_unpicked_packages_task are scheduled at
# app import time but never ran before because nothing was processing them).
# process_tasks isn't supervised by Azure App Service (only the foreground
# gunicorn process is), so if it ever exits/crashes it must be restarted here,
# otherwise scheduled reminders silently stop running forever.
(
  while true; do
    python manage.py process_tasks
    echo "[WARN] process_tasks exited (code $?), restarting in 5s..." >&2
    sleep 5
  done
) &

gunicorn mysite.wsgi --workers 2 --threads 2 --timeout 120
