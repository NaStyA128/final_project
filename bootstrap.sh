#!/usr/bin/env bash

cd /vagrant
. .env/bin/activate
cd django-project/
python manage.py runserver