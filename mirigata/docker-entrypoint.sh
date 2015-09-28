#!/usr/bin/env bash

yes yes | python manage.py migrate --noinput

#uwsgi --http :8000 --module mirigata.wsgi:application --master
uwsgi --ini /app/mirigata/docker-uwsgi.ini
