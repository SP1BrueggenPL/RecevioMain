#!/bin/bash
python manage.py migrate --noinput
gunicorn mysite.wsgi --workers 2 --threads 2 --timeout 120
