#!/bin/bash

echo "Starting server"
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata user_types
python manage.py runserver 0.0.0.0:8000
