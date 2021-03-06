#!/bin/bash

echo Migrating...
python manage.py migrate --no-input

echo Collecting static...
python manage.py collectstatic --no-input

echo Compressing styles...
python manage.py compress --engine jinja2 --force

if [[ "$ENV" == "development" ]]; then
    mkdir -p /static/media
    ./manage.py loaddata ./init/*
    ./manage.py runserver 0.0.0.0:8000
else
    uwsgi --ini /app/config.ini
fi
