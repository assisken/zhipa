#!/bin/bash

echo Migrating...
python manage.py migrate --no-input

echo Collecting static...
python manage.py collectstatic --no-input

echo Compressing styles...
python manage.py compress --engine jinja2 --force

exec $@
