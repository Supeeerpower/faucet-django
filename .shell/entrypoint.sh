#!/bin/bash
echo 'Flush the database...'
python manage.py flush --no-input
echo 'Start Migration...'
python manage.py migrate
echo "Database loaded successfully!"
python manage.py create_admin_user
echo "Admin User created successfully."
celery -A core worker -l info &
# Read the value of PROJECT_ENV environment variable
PROJECT_ENV="${PROJECT_ENV:-development}"
if [ "$PROJECT_ENV" == "production" ]; then
    python manage.py collectstatic --noinput
    gunicorn --bind 0.0.0.0:8000 core.wsgi:application
else
    python manage.py runserver 0.0.0.0:8000 --skip-checks
fi