#!/bin/bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn mysite.wsgi --workers 2 --threads 2 --timeout 60
