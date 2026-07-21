#!/bin/bash
python manage.py migrate --noinput

# django-background-tasks needs a worker process to actually consume the queue
# (close_expired_visitors_task / remind_unpicked_packages_task are scheduled at
# app import time but never ran before because nothing was processing them).
python manage.py process_tasks &

gunicorn mysite.wsgi --workers 2 --threads 2 --timeout 120
