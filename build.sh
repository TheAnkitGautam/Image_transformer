#!/usr/bin/env bash
# exit on error
export PORT=8000  # For Linux/macOS
set PORT=8000     # For Windows
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
if [[ $CREATE_SUPERUSER ]];
then
  python manage.py createsuperuser --no-input --email "$DJANGO_SUPERUSER_EMAIL"
fi