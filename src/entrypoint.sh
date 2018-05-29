#!/bin/sh
sleep 3
mkdir -p logs
./manage.py collectstatic --no-input -c
./manage.py makemigrations
./manage.py migrate
./manage.py compilemessages
supervisord -n
