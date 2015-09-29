#!/usr/bin/env bash

# wait for MIRIGATA_DB to start
WAITING=1
while [ ${WAITING} -ne 0 ]
do
    echo "Waiting for ${MIRIGATA_DB_PORT_3306_TCP_ADDR}"
    nc -z -w 30 ${MIRIGATA_DB_PORT_3306_TCP_ADDR} ${MIRIGATA_DB_PORT_3306_TCP_PORT}
    sleep 1
    nc -z -w 30 ${MIRIGATA_DB_PORT_3306_TCP_ADDR} ${MIRIGATA_DB_PORT_3306_TCP_PORT}
    WAITING=$?
done
echo "MySQL is up, starting"

# migrate database tables
yes yes | python manage.py migrate --noinput

# run uwsgi
uwsgi --ini /app/mirigata/docker-uwsgi.ini
